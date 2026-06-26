"""
Testes do parser de cores CSS (utils/color_parser.py).
"""
import pytest
from backend.utils.color_parser import parse_color, is_large_text


# =============================================================================
# parse_color
# =============================================================================

def test_rgb_valido():
    result = parse_color("rgb(255, 0, 0)")
    assert result == (1.0, 0.0, 0.0)


def test_rgba_valido():
    result = parse_color("rgba(0, 255, 0, 0.5)")
    assert result == (0.0, 1.0, 0.0)


def test_rgb_com_espacos():
    result = parse_color("rgb(0, 0, 255)")
    assert result == (0.0, 0.0, 1.0)


def test_alpha_zero_retorna_none():
    result = parse_color("rgba(255, 0, 0, 0)")
    assert result is None


def test_string_invalida_retorna_none():
    result = parse_color("invalid-color")
    assert result is None


def test_hex_nao_e_suportado_retorna_none():
    result = parse_color("#ff0000")
    assert result is None


def test_named_color_nao_e_suportado_retorna_none():
    result = parse_color("red")
    assert result is None


# =============================================================================
# is_large_text
# =============================================================================

def test_fonte_24px_e_grande():
    assert is_large_text(24.0, "400") is True


def test_fonte_18px_bold_e_grande():
    assert is_large_text(18.67, "700") is True


def test_fonte_16px_normal_nao_e_grande():
    assert is_large_text(16.0, "400") is False


def test_fonte_18px_normal_nao_e_grande():
    assert is_large_text(18.0, "400") is False


@pytest.mark.parametrize("weight", ["700", "800", "900", "bold", "bolder"])
def test_fonte_18px_com_peso_variado(weight):
    assert is_large_text(18.67, weight) is True
