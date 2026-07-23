"""
Testes do módulo de contraste (utils/contrast.py).

Testa apenas a função compute_contrast_issues, que é Python puro
(sem Playwright). A coleta dos dados do navegador é testada
indiretamente via integração.
"""

from backend.utils.contrast import compute_contrast_issues


def test_contraste_suficiente_nao_dispara_erro():
    """Preto sobre branco tem contraste de 21:1 — muito acima do mínimo."""
    elements = [
        {
            "tag": "p",
            "text": "Texto com bom contraste",
            "color": "rgb(0, 0, 0)",
            "background": "rgb(255, 255, 255)",
            "fontSize": "16px",
            "fontWeight": "400",
        }
    ]
    issues = compute_contrast_issues(elements)
    assert len(issues) == 0


def test_contraste_insuficiente_dispara_erro():
    """Cinza claro (#cccccc) sobre branco (#ffffff) tem contraste baixo."""
    elements = [
        {
            "tag": "p",
            "text": "Texto quase invisível",
            "color": "rgb(204, 204, 204)",
            "background": "rgb(255, 255, 255)",
            "fontSize": "16px",
            "fontWeight": "400",
        }
    ]
    issues = compute_contrast_issues(elements)
    assert len(issues) == 1
    assert issues[0].ratio < 4.5


def test_texto_grande_tem_limite_menor():
    """Texto grande (24px) precisa de apenas 3:1 de contraste."""
    elements = [
        {
            "tag": "h1",
            "text": "Título grande",
            "color": "rgb(170, 170, 170)",
            "background": "rgb(255, 255, 255)",
            "fontSize": "24px",
            "fontWeight": "400",
        }
    ]
    issues = compute_contrast_issues(elements)
    # 170,170,170 sobre branco dá ~1.9:1 — ainda falha mesmo para texto grande
    assert len(issues) == 1


def test_cor_invalida_ignorada():
    elements = [
        {
            "tag": "p",
            "text": "Cor inválida",
            "color": "invalid",
            "background": "rgb(255, 255, 255)",
            "fontSize": "16px",
            "fontWeight": "400",
        }
    ]
    issues = compute_contrast_issues(elements)
    assert len(issues) == 0


def test_lista_vazia_retorna_vazio():
    assert compute_contrast_issues([]) == []


def test_multiplos_elementos():
    elements = [
        {
            "tag": "p",
            "text": "Bom contraste",
            "color": "rgb(0, 0, 0)",
            "background": "rgb(255, 255, 255)",
            "fontSize": "16px",
            "fontWeight": "400",
        },
        {
            "tag": "span",
            "text": "Contraste ruim",
            "color": "rgb(200, 200, 200)",
            "background": "rgb(255, 255, 255)",
            "fontSize": "14px",
            "fontWeight": "400",
        },
    ]
    issues = compute_contrast_issues(elements)
    assert len(issues) == 1
    assert issues[0].tag == "span"
