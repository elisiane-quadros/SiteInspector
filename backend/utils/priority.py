"""
Módulo de priorização de correções de acessibilidade.

Classifica cada categoria de falha encontrada em níveis de prioridade
(P1, P2, P3) com base no impacto em segurança jurídica (LBI/WCAG),
experiência/conversão e estrutura/SEO — e gera um roadmap ordenado
para orientar o usuário sobre por onde começar as correções.
"""

# Mapeamento de prioridade por categoria de falha
PRIORITY_MAP = {
    "forms": {
        "level": "P1",
        "label": "Crítico",
        "reason": (
            "Impede o preenchimento de formulários — bloqueia cadastros, "
            "compras e contato direto. Risco direto de não conformidade com a LBI."
        ),
    },
    "focus": {
        "level": "P1",
        "label": "Crítico",
        "reason": (
            "Impede a navegação completa do site via teclado, excluindo "
            "totalmente usuários que dependem dessa tecnologia assistiva."
        ),
    },
    "buttons": {
        "level": "P2",
        "label": "Alto",
        "reason": (
            "Botões sem rótulo geram loops de navegação e frustração, "
            "aumentando a taxa de abandono."
        ),
    },
    "links": {
        "level": "P2",
        "label": "Alto",
        "reason": (
            "Links vagos prejudicam a navegação por leitores de tela e "
            "reduzem a confiança do usuário."
        ),
    },
    "contrast": {
        "level": "P2",
        "label": "Alto",
        "reason": (
            "Baixo contraste dificulta a leitura e aumenta a fadiga visual, "
            "impactando diretamente a conversão."
        ),
    },
    "screenshots": {
        "level": "P3",
        "label": "Médio",
        "reason": (
            "Imagens sem descrição afetam o SEO e a experiência de usuários com deficiência visual."
        ),
    },
    "headings": {
        "level": "P3",
        "label": "Médio",
        "reason": (
            "Hierarquia de títulos incorreta prejudica a indexação no "
            "Google e a navegação estrutural."
        ),
    },
    "landmarks": {
        "level": "P3",
        "label": "Médio",
        "reason": (
            "Ausência de landmarks dificulta a navegação rápida por tecnologias assistivas."
        ),
    },
}

# Nomes amigáveis exibidos no relatório
CATEGORY_NAMES = {
    "forms": "Campos de Formulário sem Rótulo",
    "focus": "Navegação por Teclado",
    "buttons": "Botões sem Rótulo Acessível",
    "links": "Links com Texto Vago",
    "contrast": "Contraste de Cores Insuficiente",
    "screenshots": "Imagens sem Descrição (Alt)",
    "headings": "Hierarquia de Títulos",
    "landmarks": "Landmarks Semânticos Ausentes",
}

# Ordem de exibição: P1 > P2 > P3
_PRIORITY_ORDER = {"P1": 0, "P2": 1, "P3": 2}


def generate_priority_roadmap(results: dict, contrast_issues: list) -> list[dict]:
    """
    Gera o roadmap de otimização ordenado por prioridade (P1 > P2 > P3),
    incluindo apenas categorias com ocorrências reais (count > 0).
    """
    # Computa as contagens de forma limpa
    counts = {key: len(results.get(key, [])) for key in PRIORITY_MAP if key != "contrast"}
    counts["contrast"] = len(contrast_issues)

    roadmap = []
    for category, count in counts.items():
        if count > 0:
            # Usando .get() para evitar KeyError caso o mapa mude no futuro
            info = PRIORITY_MAP.get(category)
            name = CATEGORY_NAMES.get(category, f"Outros ({category})")

            if info:
                roadmap.append(
                    {
                        "priority": info["level"],
                        "label": info["label"],
                        "category": name,
                        "count": count,
                        "reason": info["reason"],
                    }
                )

    # Ordena o roadmap com base no peso definido em _PRIORITY_ORDER
    roadmap.sort(key=lambda item: _PRIORITY_ORDER.get(item["priority"], 99))

    return roadmap
