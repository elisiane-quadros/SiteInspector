"""
Testes do motor de auditoria (scanner/core.py).

Valida cada função de verificação individualmente usando HTML
controlado, sem depender de requisições externas ou Playwright.
"""

import pytest
from bs4 import BeautifulSoup

from backend.scanner.core import (
    check_buttons_without_label,
    check_heading_structure,
    check_images_without_alt,
    check_inputs_without_label,
    check_keyboard_navigation,
    check_links_with_vague_text,
    check_missing_landmarks,
)

# =============================================================================
# check_images_without_alt
# =============================================================================


def test_imagens_com_alt_nao_disparam_erro():
    soup = BeautifulSoup('<img src="foto.jpg" alt="Descrição válida" />', "html.parser")
    issues = check_images_without_alt(soup)
    assert len(issues) == 0


def test_imagem_sem_alt_dispara_erro():
    soup = BeautifulSoup('<img src="foto.jpg" />', "html.parser")
    issues = check_images_without_alt(soup)
    assert len(issues) == 1
    assert issues[0].wcag == "1.1.1"


def test_imagem_com_alt_vazio_dispara_erro():
    soup = BeautifulSoup('<img src="foto.jpg" alt="" />', "html.parser")
    issues = check_images_without_alt(soup)
    assert len(issues) == 1


def test_multiplas_imagens_sem_alt():
    html = """
    <img src="a.jpg" alt="ok" />
    <img src="b.jpg" />
    <img src="c.jpg" alt="" />
    <img src="d.jpg" alt="ok2" />
    """
    soup = BeautifulSoup(html, "html.parser")
    issues = check_images_without_alt(soup)
    assert len(issues) == 2


# =============================================================================
# check_inputs_without_label
# =============================================================================


def test_input_com_label_nao_dispara_erro():
    html = '<label for="nome">Nome:</label><input id="nome" type="text" />'
    soup = BeautifulSoup(html, "html.parser")
    issues = check_inputs_without_label(soup)
    assert len(issues) == 0


def test_input_sem_label_dispara_erro():
    soup = BeautifulSoup('<input type="text" name="email" />', "html.parser")
    issues = check_inputs_without_label(soup)
    assert len(issues) == 1


def test_input_com_aria_label_nao_dispara_erro():
    soup = BeautifulSoup('<input type="text" aria-label="Buscar" />', "html.parser")
    issues = check_inputs_without_label(soup)
    assert len(issues) == 0


def test_input_hidden_e_ignorado():
    soup = BeautifulSoup('<input type="hidden" name="csrf" value="123" />', "html.parser")
    issues = check_inputs_without_label(soup)
    assert len(issues) == 0


def test_textarea_sem_label_dispara_erro():
    soup = BeautifulSoup('<textarea name="mensagem"></textarea>', "html.parser")
    issues = check_inputs_without_label(soup)
    assert len(issues) == 1


def test_select_sem_label_dispara_erro():
    soup = BeautifulSoup('<select name="estado"><option>SP</option></select>', "html.parser")
    issues = check_inputs_without_label(soup)
    assert len(issues) == 1


# =============================================================================
# check_heading_structure
# =============================================================================


def test_hierarquia_correta_nao_dispara_erro():
    html = "<h1>Título</h1><h2>Seção</h2><h3>Subseção</h3>"
    soup = BeautifulSoup(html, "html.parser")
    issues = check_heading_structure(soup)
    assert len(issues) == 0


def test_salto_de_nivel_dispara_erro():
    html = "<h1>Título</h1><h3>Pulou h2</h3>"
    soup = BeautifulSoup(html, "html.parser")
    issues = check_heading_structure(soup)
    assert len(issues) == 1
    assert "saltou" in issues[0].message.lower()


def test_multiplos_h1_dispara_erro():
    html = "<h1>Primeiro</h1><h1>Segundo</h1>"
    soup = BeautifulSoup(html, "html.parser")
    issues = check_heading_structure(soup)
    # Deve ter pelo menos o erro de múltiplos h1
    h1_issues = [i for i in issues if "h1" in i.element]
    assert len(h1_issues) >= 1


def test_nenhum_h1_dispara_erro():
    soup = BeautifulSoup("<h2>Seção</h2>", "html.parser")
    issues = check_heading_structure(soup)
    h1_issues = [i for i in issues if i.element == "h1"]
    assert len(h1_issues) >= 1


# =============================================================================
# check_links_with_vague_text
# =============================================================================


def test_link_descritivo_nao_dispara_erro():
    soup = BeautifulSoup(
        '<a href="/produtos">Catálogo completo de produtos</a>',
        "html.parser",
    )
    issues = check_links_with_vague_text(soup)
    assert len(issues) == 0


@pytest.mark.parametrize(
    "vague_text",
    [
        "clique aqui",
        "saiba mais",
        "leia mais",
        "acesse",
        "ver mais",
        "continue lendo",
        "detalhes",
        "clique",
    ],
)
def test_link_com_texto_vago_dispara_erro(vague_text):
    soup = BeautifulSoup(f'<a href="/page">{vague_text}</a>', "html.parser")
    issues = check_links_with_vague_text(soup)
    assert len(issues) == 1


# =============================================================================
# check_buttons_without_label
# =============================================================================


def test_botao_com_texto_nao_dispara_erro():
    soup = BeautifulSoup('<button type="submit">Enviar</button>', "html.parser")
    issues = check_buttons_without_label(soup)
    assert len(issues) == 0


def test_botao_sem_texto_dispara_erro():
    soup = BeautifulSoup('<button type="button"></button>', "html.parser")
    issues = check_buttons_without_label(soup)
    assert len(issues) == 1


def test_botao_com_aria_label_nao_dispara_erro():
    soup = BeautifulSoup('<button aria-label="Fechar"></button>', "html.parser")
    issues = check_buttons_without_label(soup)
    assert len(issues) == 0


def test_div_com_role_button_sem_label_dispara_erro():
    soup = BeautifulSoup('<div role="button" onclick="fechar()"></div>', "html.parser")
    issues = check_buttons_without_label(soup)
    assert len(issues) == 1


# =============================================================================
# check_missing_landmarks
# =============================================================================


def test_todos_landmarks_presentes():
    html = "<main><nav></nav><header></header><footer></footer></main>"
    soup = BeautifulSoup(html, "html.parser")
    issues = check_missing_landmarks(soup)
    assert len(issues) == 0


def test_landmarks_ausentes():
    soup = BeautifulSoup("<div>Conteúdo</div>", "html.parser")
    issues = check_missing_landmarks(soup)
    # Deve acusar falta de main, nav, header e footer
    assert len(issues) == 4


def test_apenas_main_presente():
    html = "<main><div>Conteúdo</div></main>"
    soup = BeautifulSoup(html, "html.parser")
    issues = check_missing_landmarks(soup)
    # Deve acusar falta de nav, header e footer
    assert len(issues) == 3
    tags_ausentes = [i.element for i in issues]
    assert "nav" in tags_ausentes
    assert "header" in tags_ausentes
    assert "footer" in tags_ausentes


# =============================================================================
# check_keyboard_navigation
# =============================================================================


def test_tabindex_positivo_dispara_warning():
    soup = BeautifulSoup('<div tabindex="5">Elemento</div>', "html.parser")
    issues = check_keyboard_navigation(soup)
    assert len(issues) == 1
    assert issues[0].severity.value == "warning"


def test_div_clickavel_sem_tabindex_dispara_erro():
    soup = BeautifulSoup('<div onclick="alert()">Clique</div>', "html.parser")
    issues = check_keyboard_navigation(soup)
    assert len(issues) == 1
    assert issues[0].severity.value == "error"


def test_link_sem_href_dispara_erro():
    soup = BeautifulSoup("<a>Link sem href</a>", "html.parser")
    issues = check_keyboard_navigation(soup)
    assert len(issues) == 1


def test_elemento_sem_problemas_nao_dispara_erro():
    html = """
    <div>Texto normal</div>
    <a href="/page">Link válido</a>
    <button type="button">Ok</button>
    """
    soup = BeautifulSoup(html, "html.parser")
    issues = check_keyboard_navigation(soup)
    assert len(issues) == 0
