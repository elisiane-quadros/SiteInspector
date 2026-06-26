from bs4 import BeautifulSoup
from backend.models.schemas import BaseIssue, Severity

# Dicionário de tradução: mapeia dados técnicos para a linguagem do cliente leigo
FRIENDLY_TEXTS = {
    "1.1.1": {
        "title": "Imagens sem descrição (Invisíveis)",
        "message": "Algumas imagens no seu site não têm uma descrição em texto. Clientes com deficiência visual que usam leitores de tela não saberão o que é exibido, o que prejudica suas vendas e o SEO do Google.",
        "how_to_fix": "No painel do seu e-commerce (WordPress/Shopify), abra a biblioteca de mídia, localize a imagem e preencha o campo 'Texto Alternativo' ou 'Alt Text'."
    },
    "1.3.1_input": {
        "title": "Campos de formulário sem nome",
        "message": "Existem campos de preenchimento (como caixas de texto ou seletores) sem uma etiqueta explicativa. O usuário não sabe o que deve digitar ali.",
        "how_to_fix": "No editor do seu site, certifique-se de que cada campo de formulário tenha um rótulo de texto (Label) visível ou um atributo descritivo (Aria-label) associado."
    },
    "1.3.1_heading_jump": {
        "title": "Títulos fora de ordem (Bagunça visual)",
        "message": "A ordem dos títulos do seu site pulou um nível (ex: pulou do título principal direto para um subtítulo pequeno). Isso confunde quem navega usando o teclado.",
        "how_to_fix": "Organize a estrutura do seu texto seguindo a ordem correta dos blocos: Heading 1 para o título principal, Heading 2 para as seções, e assim por diante."
    },
    "1.3.1_h1_count": {
        "title": "Problema com o Título Principal (H1)",
        "message": "O site possui nenhum ou múltiplos títulos principais (H1). O Google e os leitores de tela precisam de exatamente um título principal para entender o assunto da página.",
        "how_to_fix": "Modifique o layout para garantir que apenas o título mais importante da página utilize a tag H1. Mude os demais para H2 ou H3."
    },
    "2.4.4": {
        "title": "Links com textos vagos",
        "message": "Links como 'clique aqui' ou 'saiba mais' não dizem para onde o usuário será levado se clicar. Isso gera desconfiança e prejudica a experiência.",
        "how_to_fix": "Altere o texto do link para algo descritivo. Em vez de 'Clique aqui', use 'Confira nosso catálogo de produtos'."
    },
    "4.1.2": {
        "title": "Botões sem texto explicativo",
        "message": "Existem botões (muitas vezes apenas com ícones, como o carrinho ou fechar) que não possuem uma descrição em texto. O leitor de tela não consegue anunciar o que o botão faz.",
        "how_to_fix": "Adicione um texto visível ao botão ou utilize o atributo descritivo 'aria-label' no código (ex: aria-label='Adicionar ao carrinho')."
    },
    "1.3.6": {
        "title": "Estrutura de navegação incompleta",
        "message": "O site está sem marcações que dividem o topo, o conteúdo principal e o rodapé. Isso torna a navegação por teclado exaustiva e lenta.",
        "how_to_fix": "Peça para o seu desenvolvedor ou utilize temas que organizem o layout do site usando as tags padrões do HTML5 (como <header>, <main> e <footer>)."
    }
}


# WCAG 1.1.1 — Conteúdo não textual
def check_images_without_alt(soup: BeautifulSoup) -> list[BaseIssue]:
    issues = []
    texts = FRIENDLY_TEXTS["1.1.1"]

    for img in soup.find_all("img"):
        if not img.has_attr("alt") or not img["alt"].strip():
            issues.append(BaseIssue(
                wcag="1.1.1",
                severity=Severity.ERROR,
                element="img",
                message="Imagem sem texto alternativo.",
                suggestion='Adicione o atributo alt descritivo. Ex: alt="Descrição da imagem"',
                html=str(img)[:150],
                friendly_title=texts["title"],
                friendly_message=texts["message"],
                how_to_fix=texts["how_to_fix"]
            ))

    return issues


# WCAG 1.3.1 — Informação e relações
def check_inputs_without_label(soup: BeautifulSoup) -> list[BaseIssue]:
    issues = []
    ignored_types = ["hidden", "submit", "reset", "button"]
    texts = FRIENDLY_TEXTS["1.3.1_input"]

    for field in soup.find_all(["input", "textarea", "select"]):
        field_type = field.get("type", field.name)

        if field_type in ignored_types:
            continue

        field_id = field.get("id")
        label = soup.find("label", attrs={"for": field_id}) if field_id else None

        has_label = (
            label
            or field.has_attr("aria-label")
            or field.has_attr("aria-labelledby")
            or field.has_attr("title")
        )

        if not has_label:
            issues.append(BaseIssue(
                wcag="1.3.1",
                severity=Severity.ERROR,
                element=field.name,
                message=f"Campo '{field.get('name', 'sem nome')}' sem rótulo acessível.",
                suggestion='Adicione uma tag <label for="id-do-campo"> ou o atributo aria-label.',
                html=str(field)[:150],
                friendly_title=texts["title"],
                friendly_message=texts["message"],
                how_to_fix=texts["how_to_fix"]
            ))

    return issues


# WCAG 1.3.1 — Informação e relações
def check_heading_structure(soup: BeautifulSoup) -> list[BaseIssue]:
    issues = []
    last_level = 0
    h1_count = 0
    jump_texts = FRIENDLY_TEXTS["1.3.1_heading_jump"]
    h1_texts = FRIENDLY_TEXTS["1.3.1_h1_count"]

    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(heading.name[1])

        if level == 1:
            h1_count += 1

        if last_level and level > last_level + 1:
            issues.append(BaseIssue(
                wcag="1.3.1",
                severity=Severity.CRITICAL,
                element=heading.name,
                message=f"Heading saltou de <h{last_level}> para <h{level}>.",
                suggestion="Mantenha a hierarquia de headings sem saltos (ex: use <h2> após <h1>).",
                html=str(heading)[:150],
                friendly_title=jump_texts["title"],
                friendly_message=jump_texts["message"],
                how_to_fix=jump_texts["how_to_fix"]
            ))

        last_level = level

    if h1_count != 1:
        issues.insert(0, BaseIssue(
            wcag="1.3.1",
            severity=Severity.ERROR,
            element="h1",
            message=f"Encontrados {h1_count} elementos <h1>. O ideal é exatamente 1.",
            suggestion="Mantenha apenas um <h1> por página — ele representa o título principal.",
            html=None,
            friendly_title=h1_texts["title"],
            friendly_message=f"Encontramos {h1_count} títulos principais (H1) na sua página. {h1_texts['message']}",
            how_to_fix=h1_texts["how_to_fix"]
        ))

    return issues


# WCAG 2.4.4 — Propósito do link
def check_links_with_vague_text(soup: BeautifulSoup) -> list[BaseIssue]:
    vague_texts = [
        "clique aqui", "saiba mais", "leia mais", "acesse", "ver mais",
        "continue lendo", "detalhes", "mais", "aqui", "ver", "confira",
        "clique", "link", "acesse aqui", "veja mais"
    ]

    issues = []
    texts = FRIENDLY_TEXTS["2.4.4"]

    for a in soup.find_all("a"):
        text = a.get_text(strip=True).lower()

        if any(vague in text for vague in vague_texts):
            issues.append(BaseIssue(
                wcag="2.4.4",
                severity=Severity.WARNING,
                element="a",
                message=f'Link com texto genérico: "{a.get_text(strip=True)}"',
                suggestion="Descreva o destino do link. Ex: 'Leia o relatório de acessibilidade 2024' em vez de 'clique aqui'.",
                html=str(a)[:150],
                friendly_title=texts["title"],
                friendly_message=texts["message"],
                how_to_fix=texts["how_to_fix"]
            ))

    return issues


# WCAG 4.1.2 — Nome, função e valor
def check_buttons_without_label(soup: BeautifulSoup) -> list[BaseIssue]:
    issues = []
    texts = FRIENDLY_TEXTS["4.1.2"]

    clickable = soup.find_all(
        lambda tag: tag.name == "button"
        or tag.get("role") == "button"
        or "onclick" in tag.attrs
    )

    for btn in clickable:
        has_label = (
            btn.get_text(strip=True)
            or btn.has_attr("aria-label")
            or btn.has_attr("aria-labelledby")
            or btn.has_attr("title")
        )

        if not has_label:
            issues.append(BaseIssue(
                wcag="4.1.2",
                severity=Severity.ERROR,
                element=btn.name,
                message=f"<{btn.name}> sem rótulo acessível.",
                suggestion='Adicione texto visível, aria-label ou aria-labelledby. Ex: <button aria-label="Fechar menu">',
                html=str(btn)[:150],
                friendly_title=texts["title"],
                friendly_message=texts["message"],
                how_to_fix=texts["how_to_fix"]
            ))

    return issues


# WCAG 2.1.1 — Acessibilidade pelo teclado e foco
FRIENDLY_TEXTS["2.1.1"] = {
    "title": "Navegação por teclado e foco",
    "message": "Alguns elementos interativos não podem ser acessados pelo teclado ou alteram a ordem natural de tabulação.",
    "how_to_fix": "Garanta que todos os controles sejam focoáveis com tabindex=0 quando necessário e evite tabindex positivo. Elementos interativos sem semântica precisam de role e tabindex para funcionar com o teclado."
}

def check_keyboard_navigation(soup: BeautifulSoup) -> list[BaseIssue]:
    issues = []
    texts = FRIENDLY_TEXTS["2.1.1"]

    def is_non_semantic_clickable(tag):
        if tag.name in ["div", "span", "li", "td", "section"]:
            return (
                tag.has_attr("onclick")
                or tag.has_attr("onkeydown")
                or tag.get("role") in ["button", "link"]
            )
        return False

    for tag in soup.find_all(True):
        tabindex = tag.get("tabindex")

        if tabindex:
            try:
                tab_value = int(tabindex)
                if tab_value > 0:
                    issues.append(BaseIssue(
                        wcag="2.1.1",
                        severity=Severity.WARNING,
                        element=tag.name,
                        message=f"Elemento <{tag.name}> usa tabindex positivo ({tabindex}). Isso muda a ordem de navegação por teclado.",
                        suggestion="Use tabindex=0 apenas quando necessário e mantenha a ordem de tabulação natural.",
                        html=str(tag)[:150],
                        friendly_title=texts["title"],
                        friendly_message=texts["message"],
                        how_to_fix=texts["how_to_fix"]
                    ))
            except ValueError:
                pass

        if is_non_semantic_clickable(tag) and not tag.has_attr("tabindex"):
            issues.append(BaseIssue(
                wcag="2.1.1",
                severity=Severity.ERROR,
                element=tag.name,
                message=f"Elemento <{tag.name}> interativo não é focoável pelo teclado.",
                suggestion='Adicione tabindex=0 ao elemento e use role="button" ou role="link" quando necessário.',
                html=str(tag)[:150],
                friendly_title=texts["title"],
                friendly_message=texts["message"],
                how_to_fix=texts["how_to_fix"]
            ))

        if tag.name == "a" and not tag.get("href") and not tag.has_attr("tabindex"):
            if tag.get_text(strip=True):
                issues.append(BaseIssue(
                    wcag="2.1.1",
                    severity=Severity.ERROR,
                    element="a",
                    message=f"Link <a> sem href não é navegado pelo teclado.",
                    suggestion="Use href válido ou torne o elemento focoável com tabindex e role apropriados.",
                    html=str(tag)[:150],
                    friendly_title=texts["title"],
                    friendly_message=texts["message"],
                    how_to_fix=texts["how_to_fix"]
                ))

    return issues


# WCAG 1.3.6 — Identificar a finalidade
def check_missing_landmarks(soup: BeautifulSoup) -> list[BaseIssue]:
    landmarks = {
        "main": "Define o conteúdo principal da página.",
        "nav": "Define a área de navegação.",
        "header": "Define o cabeçalho da página.",
        "footer": "Define o rodapé da página."
    }

    issues = []
    texts = FRIENDLY_TEXTS["1.3.6"]

    for tag, description in landmarks.items():
        if not soup.find(tag):
            issues.append(BaseIssue(
                wcag="1.3.6",
                severity=Severity.WARNING,
                element=tag,
                message=f"Landmark <{tag}> ausente.",
                suggestion=f"Adicione a tag <{tag}> na página. {description}",
                html=None,
                friendly_title=f"{texts['title']} (<{tag}>)",
                friendly_message=f"Falta a marcação estrutural de {tag} no site. {texts['message']}",
                how_to_fix=texts["how_to_fix"]
            ))

    return issues