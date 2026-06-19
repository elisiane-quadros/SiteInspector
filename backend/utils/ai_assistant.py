import os
import asyncio
import requests
from io import BytesIO
from PIL import Image
from groq import Groq
from bs4 import BeautifulSoup
import re

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

SYSTEM_PROMPT_TEMPLATES = {
    "ecommerce": (
        "Você é um Auditor de Acessibilidade Digital e Especialista em CRO (Conversion Rate Optimization) para E-commerce.\n"
        "Sua missão é transformar cada erro técnico de acessibilidade em um impacto financeiro concreto e mensurável.\n\n"
        "Diretrizes obrigatórias:\n"
        "- Quantifique perdas: use estimativas de mercado (ex: '15% dos usuários com deficiência visual abandonam checkout sem aria-label nos botões').\n"
        "- Conecte acessibilidade a SEO: Google penaliza estrutura semântica quebrada — cite impacto em ranking orgânico.\n"
        "- Cite a LBI (Lei 13.146/2015): multas e risco de ação civil pública são argumentos decisivos para aprovação de budget.\n"
        "- Tom: direto, executivo, orientado a ROI. Sem jargão técnico desnecessário."
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
        "Sua missão é demonstrar como cada barreira de acessibilidade se traduz em perda de MRR, aumento de churn e bloqueio de expansão de mercado.\n\n"
        "Diretrizes obrigatórias:\n"
        "- Mapeie o impacto no funil de ativação: usuários que não conseguem completar o onboarding nunca ativam — zero LTV.\n"
        "- Cite o mercado endereçável perdido: 18,6 milhões de brasileiros com deficiência são usuários potenciais bloqueados.\n"
        "- Conecte acessibilidade a enterprise sales: clientes corporativos exigem conformidade WCAG em RFPs e contratos.\n"
        "- Tom: data-driven, orientado a produto e crescimento sustentável."
    )
}

async def generate_image_description(image_url: str) -> str:
    """
    Baixa uma imagem de forma assíncrona e utiliza o cliente `groq`
    para gerar uma descrição alternativa (alt text) focada em e-commerce.
    """
    if not client:
        return "Configuração de IA ausente (Chave API não encontrada no ambiente)."

    try:
        # Usamos o executor do asyncio para que a requisição HTTP (síncrona) 
        # do requests não trave o loop principal do FastAPI
        loop = asyncio.get_event_loop()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = await loop.run_in_executor(
            None, 
            lambda: requests.get(image_url, headers=headers, timeout=5, verify=False)
        )
        
        if response.status_code != 200:
            return "Não foi possível carregar a imagem para a análise de IA."
        

        image_prompt = (
            "Você é um especialista em acessibilidade digital e e-commerce. "
            "Descreva esta imagem de produto para ser usada como texto alternativo (atributo alt). "
            "Seja conciso, direto e descreva o objeto, cor, material e características principais. "
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

        # Chama o endpoint de chat/completions do Groq (sincrono, rodando no executor)
        response_ai = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                # Modelo multimodal atual da Groq (o antigo llama-3.2-11b-vision-preview foi descontinuado)
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
                temperature=0.0,
            ),
        )

        if response_ai.choices and response_ai.choices[0].message.content:
            return response_ai.choices[0].message.content.strip()
        
        return ""

    except Exception as e:
        return "Sugestão de descrição indisponível no momento."


def _extract_meta_description(html_content: str) -> str:
    """Internal helper function to extract the meta description tag from HTML via Regex."""
    if not html_content:
        return "Descrição textual indisponível."
        
    pattern = r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']'
    match = re.search(pattern, html_content, re.IGNORECASE)
    
    if not match:
        inverted_pattern = r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']'
        match = re.search(inverted_pattern, html_content, re.IGNORECASE)
        
    return match.group(1) if match else "Descrição não encontrada no HTML principal."


def _detect_business_segment(url: str, meta_description: str) -> str:
    """
    Analyzes the URL and Meta Description for keywords to classify the target
    website as 'ecommerce', 'saas', or 'corporate' (default).
    """
    analysis_text = f"{url} {meta_description}".lower()
    print(f"[SEGMENT DEBUG] Texto analisado: {analysis_text[:200]}") 
    # Busca por palavras exatas ou radicais comuns do ecossistema de vendas
    ecommerce_pattern = r"\b(compre?|lojas?|produtos?|ofertas?|descontos?|carrinho|checkout|vendas?|shop(ping)?|cart|store|roupas?|sapatos?|acessórios?|parcelado|moda|femininas?|masculinas?|infantis?)\b"
    
    # 2. PADRÃO REGEX PARA SAAS / PLATAFORMAS
    # Busca por termos que indicam sistemas baseados em assinatura, dashboards ou automações
    saas_pattern = r"\b(plataformas?|softwares?|sistemas?|apps?|automaç(ão|ões)|ferramentas?|dashboards?|mrr|saas|hub|tools?)\b"
    
    # Executa a busca via Regex
    if re.search(ecommerce_pattern, analysis_text):
        return "ecommerce"
        
    if re.search(saas_pattern, analysis_text):
        return "saas"
        
    return "corporate"


def clean_html_for_llm(html_content: str) -> str:
    """
    Remove tags pesadas e irrelevantes para análise estratégica,
    reduzindo drasticamente o consumo de tokens na API da Groq.
    """
    if not html_content:
        return ""
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove elementos que não alteram o entendimento de acessibilidade de alto nível
    for element in soup(["script", "style", "svg", "iframe", "noscript", "link"]):
        element.decompose()
        
    # Retorna o HTML limpo, removendo espaços e quebras de linha duplicadas
    cleaned_text = soup.prettify()
    return "\n".join([line.strip() for line in cleaned_text.splitlines() if line.strip()])


async def generate_executive_report(url: str, html_content: str, summary_errors: dict, business_segment: str = "corporate", roadmap: list = None) -> str:
    if not client:
        return "Configuração da IA Groq ausente."

    print(f"\n[AI DEBUG] Starting Contextualized IA Pipeline for: {url}")
    print(f"[AI DEBUG] Business Segment Received: {business_segment.upper()}")

    roadmap = roadmap or []

    # usa o segmento recebido como parâmetro — removida a chamada duplicada
    system_prompt_base = SYSTEM_PROMPT_TEMPLATES.get(
        business_segment.lower(),
        SYSTEM_PROMPT_TEMPLATES["corporate"]
    )

    # Nova abordagem: Construindo a Tabela Markdown estruturada para o LLM
    roadmap_lines = [
        "| Prioridade | Impacto | Categoria de Barreira | Ocorrências | Justificativa de Negócio |",
        "| :--- | :--- | :--- | :--- | :--- |"
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
    - Contexto: "{html_content}"
    - Erros Técnicos Computados: {summary_errors}
    """

    try:
        loop = asyncio.get_event_loop()

        response_ai = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt_complete},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
        )

        return response_ai.choices[0].message.content

    except Exception as e:
        import traceback
        print(f"[AI DEBUG] Groq pipeline failure: {e}")
        print(traceback.format_exc())
        return "Relatório de impactos de negócio indisponível no momento."    


