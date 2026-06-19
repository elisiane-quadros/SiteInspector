# 🔧 GUIA PRÁTICO: De Projeto para SaaS Professional

## Resumo: O que você tem vs O que precisa

```
┌─────────────────────────────────────────────────────────────┐
│                   HOJE (MVP Técnico)                        │
├─────────────────────────────────────────────────────────────┤
│ ✅ FastAPI bem estruturado                                  │
│ ✅ Async/Await para performance                             │
│ ✅ Groq integrado (imagens + texto)                         │
│ ✅ PDF corporativo (ExecutiveReportPDF)                     │
│ ✅ Regex para meta description                              │
│ ✅ Pydantic com validação rigorosa                          │
│                                                             │
│ ❌ Sem banco de dados (histórico/billing)                   │
│ ❌ Sem autenticação (multi-tenant)                          │
│ ❌ Sem detecção robusta de segmento                         │
│ ❌ Sem logging estruturado (debug impossível)               │
│ ❌ Sem testes (refatorar = risco)                           │
│ ❌ Sem rate limiting (API pública = caos)                   │
│ ❌ Tratamento de erro silencioso (erros lost)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 AMANHÃ (SaaS Professional)                  │
├─────────────────────────────────────────────────────────────┤
│ ✅ Tudo acima +                                             │
│ ✅ PostgreSQL (histórico + analytics)                       │
│ ✅ JWT autenticação (segurança)                             │
│ ✅ BusinessSegmentDetector (contexto de IA)                 │
│ ✅ Logging estruturado (Sentry + rastreamento)              │
│ ✅ 80%+ test coverage (CI/CD confiável)                     │
│ ✅ Rate limiting (por plano)                                │
│ ✅ Tratamento de erro robusto (retry/fallback)              │
│ ✅ Docker + GitHub Actions (deploy um-clique)              │
│ ✅ Stripe integration (monetização)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 TOP 5 PRIORIDADES (Ordem de Implementação)

### 1️⃣ LOGGING ESTRUTURADO (1 dia) ⭐ COMEÇA AQUI
**Por que primeiro?** Você vai debugar tudo o resto. Sem logging = cego.

```bash
pip install structlog python-json-logger sentry-sdk
```

**Arquivo novo:** `backend/config/logging.py`

```python
import structlog
import sentry_sdk
import logging
from pythonjsonlogger import jsonlogger

def setup_logging(app_env: str = "development"):
    # JSON logging para produção
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Sentry para tracking de erros em produção
    if app_env == "production":
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            traces_sample_rate=0.1,
            environment=app_env
        )

# Em main.py
from backend.config.logging import setup_logging
settings = get_settings()
setup_logging(settings.app_env)

# Uso em qualquer arquivo:
import structlog
logger = structlog.get_logger(__name__)

# Exemplos
logger.info("api_request_received", url=request.url, method=request.method)
logger.warning("ai_rate_limit", reset_at=error.reset_at, tags={"provider": "groq"})
logger.error("database_connection_failed", exc_info=True)
```

**Impacto:** Debug em produção, SLA monitoring, alertas automáticos

---

### 2️⃣ BANCO DE DADOS + MULTI-TENANT (3 dias)
**Por que?** Sem dados persistidos, não há SaaS.

```bash
pip install sqlalchemy psycopg2-binary alembic
```

**Estrutura:**
```
backend/
├── models/
│   ├── database.py      # ORM models
│   ├── tenant.py        # Tenant model
│   └── analysis.py      # Analysis record model
├── migrations/          # Alembic
├── db.py               # Session/engine setup
└── depends.py          # FastAPI dependencies
```

**Exemplo mínimo viável:** `backend/models/database.py`

```python
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    company_name = Column(String)
    plan = Column(String, default="free")  # free, pro, enterprise
    api_key = Column(String, unique=True, index=True)
    
    # Quotas
    monthly_analyses_limit = Column(Integer, default=10)
    analyses_used_this_month = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class AnalysisRecord(Base):
    __tablename__ = "analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True)  # FK para Tenant
    
    url = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Resultados (JSONB em prod)
    raw_results = Column(JSON)  # output do scanner
    ai_insights = Column(JSON)  # output do Groq
    
    # Métricas (para billing)
    total_issues = Column(Integer)
    groq_tokens_used = Column(Integer, default=0)
    processing_time_ms = Column(Integer)
    
    # Status
    ai_status = Column(String)  # "success", "rate_limited", "timeout"
```

**Impacto:** Histórico, multi-tenant, analytics, billing

---

### 3️⃣ BUSINESS SEGMENT DETECTOR (2 dias)
**Por que?** O coração da proposta: contexto = impacto de negócio

```python
# backend/utils/segment_detector.py

from enum import Enum
from typing import Optional
import re
import structlog

logger = structlog.get_logger(__name__)

class BusinessSegment(str, Enum):
    ECOMMERCE = "ecommerce"
    CORPORATE = "corporate"
    SAAS = "saas"
    BLOG = "blog"
    OTHER = "other"

class SegmentAnalysis:
    segment: BusinessSegment
    confidence: float  # 0.0 - 1.0
    primary_signals: list[str]  # ["has /products", "mentions sales", ...]

class BusinessSegmentDetector:
    def __init__(self):
        self.patterns = {
            "ecommerce": [
                r"loja|comprar|carrinho|checkout|produto",
                r"adicionar ao carrinho|promo|desconto|frete",
                r"paypal|boleto|crédito"
            ],
            "saas": [
                r"plano|assinatura|trial|subscribe|pricing",
                r"dashboard|api|integração|automação",
                r"gerenciar conta|usuários|permissões"
            ],
            "corporate": [
                r"quem somos|missão|visão|valores",
                r"contato|telefone|endereço|formulário",
                r"empresa|corporativo|setor público"
            ]
        }
    
    def detect(self, html: str, title: str = "", description: str = "") -> SegmentAnalysis:
        """Multi-layer segment detection com confidence scoring"""
        
        scores = {
            "ecommerce": 0.0,
            "saas": 0.0,
            "corporate": 0.0,
            "blog": 0.0,
        }
        
        # Layer 1: Meta description (peso 30%)
        if description:
            for segment, patterns in self.patterns.items():
                for pattern in patterns:
                    if re.search(pattern, description, re.IGNORECASE):
                        scores[segment] += 0.3
        
        # Layer 2: Title tag (peso 20%)
        if title:
            if "loja" in title.lower() or "comprar" in title.lower():
                scores["ecommerce"] += 0.2
            elif "dashboard" in title.lower():
                scores["saas"] += 0.2
        
        # Layer 3: HTML keywords (peso 50%)
        html_lower = html.lower()
        for segment, patterns in self.patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, html_lower, re.IGNORECASE))
                if matches > 0:
                    scores[segment] += min(0.5 * (matches / 10), 0.5)  # Cap at 0.5
        
        # Normalizar scores
        max_score = max(scores.values())
        if max_score > 0:
            scores = {k: v/max_score for k, v in scores.items()}
        
        primary = max(scores, key=scores.get)
        confidence = scores[primary]
        
        logger.info(
            "segment_detected",
            segment=primary,
            confidence=round(confidence, 2),
            scores=scores
        )
        
        return SegmentAnalysis(
            segment=BusinessSegment(primary),
            confidence=confidence,
            primary_signals=[segment for segment, score in scores.items() if score > 0.3]
        )

# Uso em main.py:
detector = BusinessSegmentDetector()

@app.post("/api/check", response_model=AnalysisResult)
async def check_accessibility(data: AnalysisRequest, db_session=Depends(get_db)):
    html = await fetch_html(str(data.url))
    
    # Detectar segmento ANTES de chamar IA
    segment_analysis = detector.detect(
        html=html,
        description=extract_meta_description(html),
        title=extract_title(html)
    )
    
    # Passar contexto para IA
    ai_results = await generate_executive_analysis(
        issues=base_results,
        segment=segment_analysis,
        html_excerpt=html[:2000]
    )
    
    # Salvar em DB
    record = AnalysisRecord(
        tenant_id=current_user.tenant_id,
        url=str(data.url),
        raw_results=base_results,
        ai_insights=ai_results,
        detected_segment=segment_analysis.segment
    )
    db_session.add(record)
    db_session.commit()
```

**Impacto:** IA contextual = 10x mais valioso

---

### 4️⃣ AUTENTICAÇÃO + RATE LIMITING (2 dias)
**Por que?** Segurança + controle de custos

```bash
pip install python-jose[cryptography] passlib[bcrypt] slowapi
```

**Arquivo:** `backend/auth.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from datetime import datetime, timedelta
import jwt
from slowapi import Limiter
from slowapi.util import get_remote_address

security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-prod")
ALGORITHM = "HS256"

def create_access_token(tenant_id: str, expires_delta: timedelta = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(days=30))
    payload = {
        "sub": tenant_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_tenant(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        tenant_id = payload.get("sub")
        if not tenant_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return tenant_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Em main.py
@app.post("/api/check")
@limiter.limit("10/minute")  # Rate limiting
async def check_accessibility(
    data: AnalysisRequest,
    request: Request,
    tenant_id: str = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    # Validar quota
    tenant = db.query(Tenant).filter_by(id=tenant_id).first()
    if tenant.analyses_used_this_month >= tenant.monthly_analyses_limit:
        raise HTTPException(status_code=429, detail="Monthly quota exceeded")
    
    # ... rest of logic
    
    tenant.analyses_used_this_month += 1
    db.commit()
```

**Impacto:** Controle de custos + monetização

---

### 5️⃣ TESTS (3 dias)
**Por que?** Refatorar sem susto, CI/CD confiável

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

**Estrutura mínima:**

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_groq():
    with patch('backend.utils.ai_assistant.client') as mock:
        yield mock

# tests/unit/test_segment_detector.py
def test_segment_detection_ecommerce():
    html = "<p>Loja online de eletrônicos. Compre agora!</p>"
    detector = BusinessSegmentDetector()
    result = detector.detect(html)
    
    assert result.segment == BusinessSegment.ECOMMERCE
    assert result.confidence > 0.5

# tests/integration/test_api_check_endpoint.py
@pytest.mark.asyncio
async def test_check_endpoint_success(client, mock_groq):
    mock_groq.chat.completions.create.return_value = AsyncMock(
        message=AsyncMock(content="AI analysis")
    )
    
    response = client.post("/api/check", json={"url": "https://example.com"})
    
    assert response.status_code == 200
    assert "results" in response.json()
```

**CI/CD:** GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=backend --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## 📊 Tabela de Implementação

| Tarefa | Duração | Dependência | Prioridade |
|--------|---------|-------------|-----------|
| Logging estruturado | 1 dia | - | 🔴 CRÍTICA |
| Database + ORM | 3 dias | Logging | 🔴 CRÍTICA |
| Segment Detector | 2 dias | Database | 🔴 CRÍTICA |
| Auth + Rate Limiting | 2 dias | Database | 🟠 ALTA |
| Tests (80% coverage) | 3 dias | Todas acima | 🟠 ALTA |
| Docker + GitHub Actions | 2 dias | Tests | 🟡 MÉDIA |
| Stripe Integration | 2 dias | Auth + Database | 🟡 MÉDIA |
| Monitoring (Grafana) | 1 dia | Logging | 🟢 BAIXA |

**Timeline Total:** 5-6 semanas para "Production-Ready"

---

## 🚀 Deploy Checklist

- [ ] `.env.example` documentado
- [ ] `docker-compose.yml` pronto (dev + prod)
- [ ] `requirements.txt` atualizado
- [ ] Database migrations (Alembic)
- [ ] README.md com diagrama de arquitetura
- [ ] API docs updated (`/docs`)
- [ ] GitHub Actions CI/CD ativa
- [ ] Sentry configurado
- [ ] Health check endpoint (`/api/health`)
- [ ] Graceful shutdown implemented

---

## 💡 Template FastAPI Production-Ready

```python
# backend/main.py (versão refatorada)

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog

from backend.config.settings import get_settings
from backend.config.logging import setup_logging
from backend.db import init_db, get_db
from backend.auth import get_current_tenant
from backend.routes import health, analysis, admin

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = get_settings()
    setup_logging(settings.app_env)
    init_db()
    logger.info("app_started", environment=settings.app_env)
    
    yield
    
    # Shutdown
    logger.info("app_shutdown")

settings = get_settings()
app = FastAPI(
    title="A11y Inspector API",
    version="3.0.0",
    lifespan=lifespan
)

# Middleware de segurança
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.get_allowed_hosts()
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(
    analysis.router,
    prefix="/api",
    dependencies=[Depends(get_current_tenant)],
    tags=["analysis"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.app_env == "development"
    )
```

---

## Final: Seu Caminho para SaaS

```
Semana 1: Database + Logging + Auth
    ↓
Semana 2: Segment Detector + Dynamic Prompts
    ↓
Semana 3: Tests (80%+ coverage)
    ↓
Semana 4: Stripe Integration + Quotas
    ↓
Semana 5: Docker + GitHub Actions + Monitoring
    ↓
Semana 6: Deploy em Render/Railway + Docs finais
    ↓
🚀 LIVE: Product SaaS profissional!
```

---

**Você está 60% do caminho. Os próximos passos são claros e viáveis. Comece pelo Logging (1 dia) e ganhe momento.**

