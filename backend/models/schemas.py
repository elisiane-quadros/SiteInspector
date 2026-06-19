from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional,Union, Any
from enum import Enum


class AnalysisRequest(BaseModel):
    url: HttpUrl


class Severity(str, Enum):
    CRITICAL = "critical"  # Erros que bloqueiam o usuário (ex: formulário sem label)
    ERROR = "error"        # Erros padrão de conformidade (ex: contraste baixo)
    WARNING = "warning"    # Avisos/Boas práticas (ex: pular hierarquia de heading)
    INFO = "info"          # Elementos para revisão manual


class BaseIssue(BaseModel):
    wcag: str
    severity: Severity
    element: str
    message: str
    suggestion: str
    html: Optional[str] = None

    friendly_title: Optional[str] = None    # Nome comercial (ex: "Texto difícil de ler")
    friendly_message: Optional[str] = None  # Explicação do impacto em vendas/uso
    how_to_fix: Optional[str] = None        # Instrução prática de painel (WordPress/Shopify)


class ContrastIssue(BaseModel):
    wcag: str = "1.4.3"
    severity: Severity = Severity.ERROR
    tag: str
    text: str
    color: str
    background: str
    ratio: float
    threshold: float
    message: str


class ImageAccessibilityIssue(BaseIssue):
    wcag: str
    severity: str
    element: str
    message: str
    suggestion: str
    html: str
    friendly_title: Optional[str] = None
    friendly_message: Optional[str] = None
    how_to_fix: Optional[str] = None
    image_url: Optional[str] = None  
    ai_description_suggestion: Optional[str] = None  

class AnalysisResult(BaseModel):
    success: bool
    url: str
    results: dict[str, List[Union[ImageAccessibilityIssue, BaseIssue, Any]]]
    contrast_issues: List[ContrastIssue] = []
    image_issues: List[ImageAccessibilityIssue] = []
    total_issues: int = 0
    business_segment: str
    executive_analysis: str
    priority_roadmap: List[Dict[str, Any]] = []  # ← seção separada e isolada