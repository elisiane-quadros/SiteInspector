import re
from typing import Optional

RGBTuple = tuple[float, float, float]


# Converte string de cor CSS para tupla RGB normalizada (0.0 a 1.0)
def parse_color(color_str: str) -> Optional[RGBTuple]:
    match = re.match(
        r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)",
        color_str.strip()
    )

    if not match:
        return None

    r = int(match.group(1))
    g = int(match.group(2))
    b = int(match.group(3))
    alpha = float(match.group(4)) if match.group(4) else 1.0

    if alpha == 0:
        return None

    return (r / 255, g / 255, b / 255)


# Verifica se o texto é grande segundo os critérios da WCAG
def is_large_text(font_size_px: float, font_weight: str) -> bool:
    is_bold = font_weight in ("700", "800", "900", "bold", "bolder")
    return font_size_px >= 24 or (is_bold and font_size_px >= 18.67)