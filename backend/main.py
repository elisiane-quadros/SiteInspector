from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
import sys
import urllib3

from backend.config.settings import get_settings
from backend.models.schemas import AnalysisRequest, AnalysisResult, ImageAccessibilityIssue
from backend.scanner.core import (
    check_images_without_alt,
    check_inputs_without_label,
    check_heading_structure,
    check_links_with_vague_text,
    check_buttons_without_label,
    check_missing_landmarks,
    check_keyboard_navigation
)
from backend.utils.html_fetcher import browser_session
from backend.utils.contrast import check_text_contrast
from backend.utils.priority import generate_priority_roadmap
from backend.utils.ai_assistant import (
    _detect_business_segment,
    generate_executive_report,
    generate_image_description
)

# Apenas aplica correção de event loop no Windows (necessário para Playwright)
if sys.platform == "win32":
    import nest_asyncio
    nest_asyncio.apply()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
settings = get_settings()

# --- Controle do pipeline de descrição de imagens por IA ---
# Evita que páginas com muitas imagens (ex.: e-commerce) travem a requisição:
# limita quantas imagens vão à IA, quantas rodam em paralelo e o tempo máximo de cada uma.
AI_IMAGE_LIMIT = 10          # máximo de imagens enviadas à IA por análise
AI_IMAGE_CONCURRENCY = 4     # chamadas simultâneas à IA
AI_IMAGE_TIMEOUT = 20        # segundos máximos por imagem
AI_IMAGE_FALLBACK = (
    "Esta imagem não possui o atributo 'alt'. Adicione uma descrição curta e objetiva "
    "do conteúdo ou da função da imagem para leitores de tela."
)

app = FastAPI(
    title="A11y Inspector API",
    description="API para análise automatizada de acessibilidade digital.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/check", response_model=AnalysisResult)
async def check_accessibility(data: AnalysisRequest):
    async with browser_session() as page:
        try:
            await page.goto(str(data.url),wait_until="networkidle",timeout=settings.request_timeout * 1000)
            html = await page.content()
            soup = BeautifulSoup(html, "lxml")

            # 1. Executa as análises padrão do BeautifulSoup
            base_images = check_images_without_alt(soup)

            results = {
                "focus": check_keyboard_navigation(soup),
                "forms": check_inputs_without_label(soup),
                "headings": check_heading_structure(soup),
                "links": check_links_with_vague_text(soup),
                "buttons": check_buttons_without_label(soup),
                "landmarks": check_missing_landmarks(soup),
            }

            image_records: list[list] = []
            ai_targets: list[int] = []  # índices que ainda precisam de descrição via IA

            for issue in base_images:
                # Extrai o atributo src="" da tag <img> capturada pelo BeautifulSoup
                image_url = None
                temp_soup = BeautifulSoup(issue.html, "html.parser")
                img_tag = temp_soup.find("img")
                if img_tag and img_tag.get("src"):
                    image_url = img_tag.get("src").strip()

                suggestion = None
                if image_url:
                    # Converte caminhos relativos em absolutos
                    if not image_url.startswith("http"):
                        base_url = str(data.url) if str(data.url).startswith("http") else "https://example.com"
                        image_url = urljoin(base_url, image_url)
                    # Ícones vetoriais não precisam de IA
                    if image_url.lower().split('?')[0].endswith('.svg'):
                        suggestion = "Ícones decorativos ou formatos vetoriais não requerem análise assistida por IA."
                else:
                    suggestion = "Não foi possível extrair um link de imagem válido para análise."

                idx = len(image_records)
                image_records.append([issue, image_url, suggestion])
                if suggestion is None:
                    ai_targets.append(idx)

            # 3. Gera as descrições por IA em PARALELO, com teto, concorrência limitada e timeout
            #    por imagem — assim páginas com muitas imagens não travam a requisição.
            #    Imagens acima do teto recebem o texto-guia padrão (sem chamada de IA).
            for idx in ai_targets[AI_IMAGE_LIMIT:]:
                image_records[idx][2] = AI_IMAGE_FALLBACK

            selected = ai_targets[:AI_IMAGE_LIMIT]
            if selected:
                semaphore = asyncio.Semaphore(AI_IMAGE_CONCURRENCY)

                async def describe(target_idx: int):
                    url = image_records[target_idx][1]
                    async with semaphore:
                        try:
                            text = await asyncio.wait_for(
                                generate_image_description(url),
                                timeout=AI_IMAGE_TIMEOUT,
                            )
                        except Exception:
                            text = AI_IMAGE_FALLBACK
                        return target_idx, text

                for target_idx, text in await asyncio.gather(*(describe(i) for i in selected)):
                    image_records[target_idx][2] = text

            # 4. Monta os objetos finais estendendo a BaseIssue que veio do core.py
            image_issues: list[ImageAccessibilityIssue] = []
            for issue, image_url, suggestion in image_records:
                image_issues.append(ImageAccessibilityIssue(
                    wcag=issue.wcag,
                    severity=issue.severity,
                    element=issue.element,
                    message=issue.message,
                    suggestion=issue.suggestion,
                    html=issue.html,
                    friendly_title=issue.friendly_title,
                    friendly_message=issue.friendly_message,
                    how_to_fix=issue.how_to_fix,
                    image_url=image_url,
                    ai_description_suggestion=suggestion,
                ))

            results["screenshots"] = image_issues

            # 3. Executa a análise de contraste
            contrast_issues = await check_text_contrast(page)
            results["contrast"] = contrast_issues

            # 4. Calcula o total unificado de falhas
            total_issues = sum(len(v) for v in results.values())

            # 5. Gera o roadmap de otimização ordenado por prioridade
            priority_roadmap = generate_priority_roadmap(results, contrast_issues)
            results["priority_roadmap"] = priority_roadmap

            meta_tag = soup.find("meta", attrs={"name": "description"})
            meta_description = meta_tag.get("content", "") if meta_tag else ""

            # Executa a detecção estável do nicho
            detected_segment = _detect_business_segment(str(data.url), meta_description)

            summary_errors = {
                "imagens_sem_alt": len(results.get("screenshots", [])),
                "campos_sem_rotulo": len(results.get("forms", [])),
                "hierarquia_titulos": len(results.get("headings", [])),
                "links_vagos": len(results.get("links", [])),
                "botoes_inacessiveis": len(results.get("buttons", [])),
                "landmarks_ausentes": len(results.get("landmarks", [])),
                "navegacao_teclado": len(results.get("focus", [])),
            }

            # Invoca a API da Groq para gerar o relatório estratégico de 2ª página do PDF
            ai_report = await generate_executive_report(str(data.url), meta_description, summary_errors, detected_segment,priority_roadmap)

            return AnalysisResult(
                success=True,
                url=str(data.url),
                results=results,
                contrast_issues=contrast_issues,
                image_issues=image_issues,
                total_issues=total_issues,
                business_segment=detected_segment,
                executive_analysis=ai_report,
                priority_roadmap=priority_roadmap
            )

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {
        "status": "online",
        "app": "A11y Inspector API",
        "version": "2.0.0",
        "docs": "/docs"
    }