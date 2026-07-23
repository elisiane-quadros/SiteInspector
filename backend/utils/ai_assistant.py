import asyncio
import logging
import re

from groq import Groq

from backend.config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None

SYSTEM_PROMPT_TEMPLATES = {
    "ecommerce": (
        "Você é um Auditor de Acessibilidade Digital e Especialista em CRO (Conversion Rate Optimization) para E-commerce.\n"
        "Sua missão é transformar cada erro técnico de acessibilidade em impacto de negócio concreto e compreensível.\n\n"
        "Diretrizes obrigatórias:\n"
        "- Conecte cada barreira a perda de conversão de forma qualitativa: abandono de checkout, exclusão de compradores com deficiência, fricção no funil de compra.\n"
        "- Conecte acessibilidade a SEO: Google penaliza estrutura semântica quebrada — cite impacto em ranking orgânico.\n"
        "- Cite a LBI (Lei 13.146/2015): multas e risco de ação civil pública são argumentos decisivos para aprovação de budget.\n"
        "- Tom: direto, executivo, orientado a resultado. Sem jargão técnico desnecessário."
    ),
    "corporate": (
        "Você é um Consultor Sênior de Compliance Digital, ESG e Acessibilidade para empresas de médio e grande porte.\n"
        "Sua missão é traduzir falhas técnicas em riscos institucionais concretos que impactam a reputação e o valuation da marca.\n\n"
        "Diretrizes obrigatórias:\n"
        "- Enquadre cada falha como risco ESG: investidores e parceiros B2B avaliam diversidade e inclusão digital.\n"
        "- Cite exposição legal pela LBI (Lei 13.146/2015) e WCAG 2.1: notificações do MPF e ações civis são realidade no Brasil.\n"
        "- Impacto em captação de leads: formulários inacessíveis excluem diretamente potenciais clientes com deficiência.\n"
        "- Tom: formal, estratégico, orientado a gestão de riscos corporativos."
    ),
    "saas": (
        "Você é um Growth Product Manager especialista em Acessibilidade e Retenção de Produtos SaaS B2B e B2C.\n"
        "Sua missão é demonstrar como cada barreira de acessibilidade se traduz em perda de receita recorrente, aumento de churn e bloqueio de expansão de mercado.\n\n"
        "Diretrizes obrigatórias:\n"
        "- Mapeie o impacto no funil de ativação: usuários que não conseguem completar o onboarding nunca ativam.\n"
        "- Cite o mercado endereçável perdido: 18,6 milhões de brasileiros com deficiência (IBGE) são usuários potenciais bloqueados.\n"
        "- Conecte acessibilidade a enterprise sales: clientes corporativos exigem conformidade WCAG em RFPs e contratos.\n"
        "- Tom: data-driven, orientado a produto e crescimento sustentável."
    ),
}


async def generate_image_description(image_url: str) -> str:
    """Gera descrição alternativa (alt text) para uma imagem via Groq."""
    if not client:
        return "Configuração de IA ausente (Chave API não encontrada no ambiente)."

    try:
        # O SDK do Groq é síncrono; rodamos a chamada num executor para não
        # travar o loop de eventos do FastAPI. O próprio Groq busca a imagem
        # pela URL, então não baixamos os bytes aqui.
        loop = asyncio.get_running_loop()

        image_prompt = (
            "Você é um especialista em acessibilidade digital. "
            "Descreva esta imagem para ser usada como texto alternativo (atributo alt). "
            "Seja conciso e objetivo: descreva o conteúdo principal, o contexto e "
            "qualquer texto visível na imagem. "
            "Responda estritamente com a descrição final em português, sem introduções ou frases como 'Esta imagem mostra'."
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}},
                    {"type": "text", "text": image_prompt},
                ],
            }
        ]

        response_ai = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=settings.groq_vision_model,
                messages=messages,
                temperature=0.0,
            ),
        )

        if response_ai.choices and response_ai.choices[0].message.content:
            return response_ai.choices[0].message.content.strip()

        return ""

    except Exception:
        logger.exception("Falha ao gerar descrição de imagem via Groq (url=%s)", image_url)
        return "Sugestão de descrição indisponível no momento."


def _detect_business_segment(url: str, meta_description: str) -> str:
    """
    Analisa a URL e a meta description em busca de palavras-chave para
    classificar o site alvo como 'ecommerce', 'saas' ou 'corporate' (padrão).
    """
    analysis_text = f"{url} {meta_description}".lower()

    # E-commerce: palavras exatas ou radicais comuns do ecossistema de vendas
    ecommerce_pattern = r"\b(compre?|lojas?|produtos?|ofertas?|descontos?|carrinho|checkout|vendas?|shop(ping)?|cart|store|roupas?|sapatos?|acessórios?|parcelado|moda|femininas?|masculinas?|infantis?)\b"

    # SaaS / plataformas: termos de sistemas por assinatura, dashboards ou automações
    saas_pattern = r"\b(plataformas?|softwares?|sistemas?|apps?|automaç(ão|ões)|ferramentas?|dashboards?|mrr|saas|hub|tools?)\b"

    if re.search(ecommerce_pattern, analysis_text):
        return "ecommerce"

    if re.search(saas_pattern, analysis_text):
        return "saas"

    return "corporate"


async def generate_executive_report(
    url: str,
    context: str,
    summary_errors: dict,
    business_segment: str = "corporate",
    roadmap: list = None,
) -> str:
    if not client:
        return "Configuração da IA Groq ausente."

    roadmap = roadmap or []

    system_prompt_base = SYSTEM_PROMPT_TEMPLATES.get(
        business_segment.lower(), SYSTEM_PROMPT_TEMPLATES["corporate"]
    )

    # Tabela Markdown estruturada como guia de priorização para o LLM
    roadmap_lines = [
        "| Prioridade | Impacto | Categoria de Barreira | Ocorrências | Justificativa de Negócio |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for item in roadmap:
        line = f"| {item['priority']} | {item['label']} | {item['category']} | {item['count']} | {item['reason']} |"
        roadmap_lines.append(line)

    roadmap_str = "\n".join(roadmap_lines)

    system_prompt_complete = (
        f"{system_prompt_base}\n\n"
        "Instruções estritas de Resposta:\n"
        f"DADOS DE PRIORIZAÇÃO (Use como guia de análise):\n{roadmap_str}\n\n"
        "IMPORTANTE: Comece DIRETAMENTE pelo tópico '1. Impacto em Conversão e Usuários'. "
        "Não adicione títulos introdutórios, cabeçalhos ou textos antes do primeiro tópico.\n"
        "IMPORTANTE: Não mencione valores financeiros, estimativas em R$ ou percentuais inventados. "
        "Descreva os impactos de forma qualitativa e estratégica, sem fabricar números.\n"
        "Gere o relatório dividido nestes três tópicos:\n"
        "1. Impacto em Conversão e Usuários\n"
        "2. Impacto em Tráfego e SEO\n"
        "3. Exposição Legal e Riscos de Compliance (LBI)\n\n"
        "Seja direto, extremamente persuasivo e use estritamente a volumetria de erros fornecida."
    )

    user_prompt = f"""
    Dados Coletados da Auditoria:
    - URL do Site: {url}
    - Contexto: "{context}"
    - Erros Técnicos Computados: {summary_errors}
    """

    try:
        loop = asyncio.get_running_loop()

        response_ai = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=settings.groq_report_model,
                messages=[
                    {"role": "system", "content": system_prompt_complete},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=1000,
            ),
        )

        return response_ai.choices[0].message.content

    except Exception:
        logger.exception("Falha no pipeline Groq do relatório executivo (url=%s)", url)
        return "Relatório de impactos de negócio indisponível no momento."
