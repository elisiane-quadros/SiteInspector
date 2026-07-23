from wcag_contrast_ratio import rgb

from backend.models.schemas import ContrastIssue
from backend.utils.color_parser import is_large_text, parse_color

# Script executado no navegador para coletar texto + cores computadas dos elementos
# visíveis. Roda dentro da mesma sessão de render usada pela análise estrutural
# (ver html_fetcher.fetch_page) — assim a página é carregada uma única vez.
CONTRAST_JS = """
    (maxEl) => {
        const tags = ["p","h1","h2","h3","h4","h5","h6","a","span","li","label","button"];
        return Array.from(document.querySelectorAll(tags.join(",")))
            .filter(el => {
                const s = window.getComputedStyle(el);
                return el.innerText.trim()
                    && s.display !== "none"
                    && s.visibility !== "hidden"
                    && s.opacity !== "0";
            })
            .slice(0, maxEl)
            .map(el => {
                const s = window.getComputedStyle(el);
                return {
                    tag: el.tagName.toLowerCase(),
                    text: el.innerText.trim().substring(0, 50),
                    color: s.color,
                    background: s.backgroundColor,
                    fontSize: s.fontSize,
                    fontWeight: s.fontWeight
                };
            });
    }
"""


# WCAG 1.4.3 — Contraste mínimo
# Calcula as falhas a partir das cores JÁ extraídas do navegador (Python puro,
# sem abrir nenhum navegador aqui). A coleta das cores acontece no render único.
def compute_contrast_issues(elements_data: list) -> list[ContrastIssue]:
    issues = []

    for data in elements_data or []:
        fg = parse_color(data["color"])
        bg = parse_color(data["background"])

        if fg is None or bg is None:
            continue

        ratio = rgb(fg, bg)

        font_size = float(data["fontSize"].replace("px", ""))
        font_weight = data["fontWeight"]
        threshold = 3.0 if is_large_text(font_size, font_weight) else 4.5

        if ratio < threshold:
            issues.append(
                ContrastIssue(
                    tag=data["tag"],
                    text=data["text"],
                    color=data["color"],
                    background=data["background"],
                    ratio=round(ratio, 2),
                    threshold=threshold,
                    message=f"Contraste insuficiente: {round(ratio, 2)}:1 (mínimo {threshold}:1)",
                )
            )

    return issues


async def check_text_contrast(page):
    """
    Coleta dados da página renderizada via Playwright e processa falhas de contraste.
    """
    try:
        # Executa o CONTRAST_JS na página aberta e recebe o array de elementos
        elements_data = await page.evaluate(CONTRAST_JS)

        # Processa os resultados usando sua função existente
        return compute_contrast_issues(elements_data)
    except Exception as e:
        print(f"Erro ao processar análise de contraste: {e}")
        return []
