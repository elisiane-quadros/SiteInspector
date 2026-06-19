<div align="center">

# 🌐 SiteInspector 🔍

### Plataforma de Auditoria de Acessibilidade Digital com Inteligência Artificial

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-TypeScript-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Playwright](https://img.shields.io/badge/Playwright-Headless-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![Groq](https://img.shields.io/badge/IA-Groq%20Llama-F55036?style=for-the-badge)](https://groq.com)
[![WCAG](https://img.shields.io/badge/WCAG-2.1-7B2D8B?style=for-the-badge)](https://www.w3.org/WAI/WCAG21/quickref/)
[![LBI](https://img.shields.io/badge/LBI-Lei%2013.146%2F2015-009c3b?style=for-the-badge)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> Detecta falhas de acessibilidade em tempo real, gera relatórios PDF profissionais e traduz problemas técnicos em **impacto de negócio** — com análise estratégica gerada por IA adaptada ao segmento do site.

<br/>


## 🖥️ Interface e Funcionalidades

### 1. Painel de Resultados da Inspeção
![Resultado da Inspeção](assets/resultado_inspecao_online.jpg)
> Após inserir a URL, o painel exibe todas as categorias auditadas com status visual imediato — verde para conformidade e vermelho para problemas encontrados. Dois botões de exportação geram os relatórios PDF diretamente no browser.

---

### 2. Card Detalhado de Inconformidade — com IA
![Card Detalhado](assets/card_detalhado.png)
> Ao clicar em "Ver mais", o card expande com a descrição do impacto em linguagem de negócio, orientação de correção e — para imagens — uma **sugestão de texto alternativo gerada automaticamente pelo modelo multimodal da Groq**. A seção técnica traz o snippet HTML afetado e o critério WCAG violado.

---

### 3. Relatório Executivo — Diagnóstico e Volumetria
![Relatório Executivo Página 1](assets/resultado_inspecao.png)
> Documento PDF profissional com diagnóstico de exposição legal, classificação de risco (Crítico / Moderado / Baixo) e tabela consolidada de barreiras encontradas — pronto para apresentação a gestores e equipes de compliance.

---

### 4. Relatório Executivo — Análise Estratégica gerada por IA
![Análise Estratégica IA](assets/diagnostico_ia.png)
> A segunda página do relatório traz uma análise de impacto de negócio gerada pelo **Llama 3.3 70B via Groq**, adaptada automaticamente ao segmento detectado do site (e-commerce, SaaS ou corporativo). Traduz falhas técnicas em consequências reais: perda de conversão, queda de SEO e exposição à LBI.

---

### 5. Roadmap de Otimização Sugerido — P1 / P2 / P3
![Roadmap de Prioridades](assets/roadmaps_prioridades.png)
> Classificação determinística das falhas em três níveis de prioridade, com justificativa de impacto para cada categoria. Orienta a equipe técnica sobre por onde começar para obter o maior ganho de conversão e reduzir a exposição legal imediata.
</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Diferenciais Técnicos](#-diferenciais-técnicos--decisões-de-engenharia)
- [Funcionalidades](#-funcionalidades)
- [Tech Stack](#-tech-stack)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Execução](#-instalação-e-execução)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Relatórios PDF](#-relatórios-pdf)
- [Deploy](#-deploy)
- [Roadmap](#-roadmap)
- [Autora](#-autora)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

**InclusionWeb** é uma solução web full-stack para automação de auditoria de acessibilidade digital, desenvolvida em conformidade com as diretrizes [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/) e a [Lei Brasileira de Inclusão (LBI — Lei 13.146/2015)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm).

O projeto une **engenharia de software**, **automação web (RPA)** e **Inteligência Artificial multimodal** para não apenas detectar falhas em tempo real, mas gerar sugestões de correção contextualizadas e relatórios estratégicos adaptados ao perfil do negócio.

### O grande diferencial: Dualidade de Público

| Público | Entrega |
|--------|---------|
| 👔 Gestores / Compliance | Relatório Executivo com impacto em conversão, SEO e risco legal |
| 👩‍💻 Desenvolvedores / TI | Checklist Técnico com snippets HTML, critérios WCAG e orientações de correção |

---

## 🏗️ Diferenciais Técnicos & Decisões de Engenharia

### ⚡ Pipeline Assíncrono com Controle de Concorrência
Operações de I/O bloqueantes (scraping, downloads de mídia, chamadas a APIs externas) são gerenciadas com `asyncio`, `asyncio.Semaphore` e `asyncio.wait_for`, garantindo escalabilidade sem travar o loop de eventos do FastAPI.

### 🤖 Integração com LLMs via Groq (Baixa Latência)
O backend consome dois modelos distintos via API da Groq:
- `llama-3.3-70b-versatile` — geração do **relatório executivo estratégico**, contextualizado por segmento de negócio detectado automaticamente (e-commerce, SaaS ou corporativo)
- `llama-3.2-11b-vision-preview` — **geração automática de texto alternativo** (`alt`) para imagens sem descrição, via análise multimodal

### 🔍 Renderização Real com Playwright
A análise de contraste de cores e o parsing de SPAs (React, Vue, Angular) utilizam o **Playwright** em modo *headless*, garantindo que o DOM analisado seja o DOM real renderizado pelo navegador — não o HTML estático.

### 🏗️ Validação e Serialização com Pydantic
Implementação baseada em herança de classes (`BaseIssue` → `ImageAccessibilityIssue`) com tipagem combinatória (`Union`). Impede perda de propriedades específicas de IA durante a serialização de payloads JSON complexos.

### 📊 Roadmap de Prioridades Determinístico
Classificação das falhas em **P1 / P2 / P3** calculada em Python puro (sem IA), baseada no impacto real de cada categoria:
- **P1 Crítico** — Risco legal direto / bloqueio total de uso
- **P2 Alto** — Impacto em conversão e experiência
- **P3 Médio** — Estrutura, SEO e semântica

---

## ✨ Funcionalidades

- 🖼️ **Auditoria de Imagens com IA** — Detecção de `alt` ausente + geração automática de descrição via modelo multimodal da Groq
- 📝 **Validação de Formulários** — Campos sem `<label>`, `aria-label`, `aria-labelledby` ou `title`
- 🔤 **Hierarquia de Títulos** — Verificação da árvore `<h1>` a `<h6>`, incluindo saltos de nível e múltiplos `<h1>`
- 🔗 **Links com Texto Vago** — Detecção de âncoras com texto genérico ("clique aqui", "saiba mais")
- 🖱️ **Botões Inacessíveis** — Identificação de botões sem rótulo acessível ou `aria-label`
- ⌨️ **Navegação por Teclado** — Detecção de `tabindex` positivo e elementos interativos não focáveis
- 🏛️ **Landmarks Semânticos** — Verificação de `<main>`, `<nav>`, `<header>` e `<footer>`
- 🎨 **Contraste de Cores** — Análise dinâmica de legibilidade (WCAG 1.4.3) com Playwright
- 📊 **Roadmap de Prioridades** — Classificação P1/P2/P3 com justificativa de impacto de negócio
- 🤖 **Relatório Executivo com IA** — Análise estratégica gerada pela Groq, adaptada ao segmento detectado
- 📄 **Dois Relatórios em PDF** — Executivo (gestão/compliance) e Técnico (engenharia/TI), gerados no client-side

---

## 🛠️ Tech Stack

### Backend
| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.11+ | Linguagem principal |
| FastAPI | 0.136 | API REST assíncrona |
| Playwright | 1.60 | Renderização headless e análise de contraste |
| BeautifulSoup4 + lxml | latest | Parsing de HTML estruturado |
| httpx | 0.28 | Fetch HTTP assíncrono com fallback para Playwright |
| Groq SDK | 1.4 | Integração com LLMs (relatório + visão) |
| Pydantic + Pydantic Settings | 2.x | Validação de dados e configuração via `.env` |
| wcag-contrast-ratio | 0.9 | Cálculo de contraste WCAG |

### Frontend
| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| React | 18+ | Interface baseada em componentes |
| TypeScript | 5+ | Tipagem estática |
| Tailwind CSS | 3+ | Estilização responsiva |
| Axios | latest | Consumo da API |
| @react-pdf/renderer | latest | Geração de PDF no client-side |

---

## 📂 Estrutura do Projeto

```text
SiteInspector/
├── Dockerfile                        # Configuração para deploy com suporte ao Playwright
├── run.py                            # Ponto de entrada: carrega .env e inicia o Uvicorn
├── requirements.txt
├── .env.example                      # Template de variáveis de ambiente
│
├── backend/
│   ├── main.py                       # Endpoints FastAPI e orquestração do pipeline
│   ├── config/
│   │   └── settings.py               # Configurações via Pydantic Settings
│   ├── models/
│   │   └── schemas.py                # Contratos de dados (BaseIssue, AnalysisResult, etc.)
│   ├── scanner/
│   │   └── core.py                   # Motor de auditoria (imagens, forms, headings, foco, landmarks)
│   └── utils/
│       ├── ai_assistant.py           # Pipeline Groq (relatório executivo + visão multimodal)
│       ├── contrast.py               # Análise de contraste via Playwright (WCAG 1.4.3)
│       ├── color_parser.py           # Parsing de cores CSS
│       ├── html_fetcher.py           # Fetch com fallback httpx → Playwright
│       └── priority.py               # Geração do roadmap de prioridades (P1/P2/P3)
│
├── frontend/
│   ├── .env                          # Variáveis locais (não versionado)
│   ├── .env.production               # Variáveis de produção (Vercel)
│   └── src/
│       ├── components/
│       │   ├── UrlForm.tsx
│       │   ├── ResultCard.tsx
│       │   ├── ExecutiveReportPDF.tsx # PDF para gestão / compliance
│       │   └── TechnicalReportPDF.tsx # PDF para engenharia / TI
│       ├── interfaces/               # Contratos TypeScript espelhando os schemas do backend
│       │   ├── AccessibilityResults.ts
│       │   ├── ResultItem.ts
│       │   └── ResultContrast.ts
│       ├── services/
│       │   └── api.ts                # Cliente Axios configurado
│       └── App.tsx
│
└── tests/
    ├── __init__.py
    └── test_regex.py
```

---

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/elisiane-quadros/SiteInspector.git
cd SiteInspector
```

### 2. Configurar o Backend

```bash
# Criar e ativar o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Instalar os binários do Playwright
playwright install chromium
```

### 3. Configurar as Variáveis de Ambiente

```bash
# Copie o template
cp .env.example .env

# Edite o .env e preencha sua chave da Groq
# GROQ_API_KEY=sua_chave_aqui
```

### 4. Iniciar o Backend

```bash
python run.py
```

Backend disponível em: `http://localhost:8000`  
Documentação Swagger: `http://localhost:8000/docs`

### 5. Configurar e Iniciar o Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend disponível em: `http://localhost:5173`

---

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `APP_ENV` | Ambiente da aplicação | `development` |
| `ALLOWED_ORIGINS` | URLs com permissão de chamar a API (separadas por vírgula) | `http://localhost:5173` |
| `MAX_ELEMENTS` | Máximo de elementos analisados por página | `200` |
| `REQUEST_TIMEOUT` | Timeout em segundos para fetch HTTP | `30` |
| `GROQ_API_KEY` | Chave da API Groq ([obter aqui](https://console.groq.com)) | — |

---

## 📄 Relatórios PDF

A aplicação gera dois documentos distintos, renderizados no client-side com `@react-pdf/renderer`:

### 📊 Relatório Executivo
Voltado a **gestores e compliance**. Contém:
- Diagnóstico de exposição legal (LBI / WCAG 2.1)
- Volumetria de barreiras por categoria
- Roadmap de otimização P1/P2/P3
- Análise estratégica de impacto gerada por IA (segmentada por nicho)

### 🔧 Checklist Técnico
Voltado a **engenharia e TI**. Contém:
- Lista detalhada de ocorrências por categoria
- Snippet HTML do elemento com problema
- Critério WCAG violado
- Orientação técnica de correção

---

## ☁️ Deploy

| Camada | Plataforma | Observação |
|--------|-----------|------------|
| Backend | [Railway](https://railway.app) | Suporte a Docker — necessário para o Playwright |
| Frontend | [Vercel](https://vercel.com) | Deploy automático via GitHub |

### Variáveis necessárias no Railway:
```
GROQ_API_KEY=sua_chave_aqui
ALLOWED_ORIGINS=https://seu-projeto.vercel.app
APP_ENV=production
```

### Variável necessária na Vercel:
```
VITE_API_URL=https://seu-backend.up.railway.app/api
```

---

## 🗺️ Roadmap

- [x] Auditoria de acessibilidade (WCAG 2.1)
- [x] Análise de contraste com Playwright
- [x] Geração de PDF — Relatório Executivo e Checklist Técnico
- [x] Integração com Groq (relatório estratégico + visão multimodal)
- [x] Detecção automática de segmento de negócio
- [x] Roadmap de prioridades P1/P2/P3
- [ ] Autenticação de usuários (JWT)
- [ ] Dashboard com histórico de scans
- [ ] Monitoramento contínuo com alertas por e-mail
- [ ] Plano Pro com API pública
- [ ] Unificação do browser Playwright (fetch + contraste em uma única sessão)

---

## 👩‍💻 Autora

<div align="center">

**Elisiane Quadros**

Desenvolvedora Python | IA & Automação aplicadas a Dados e Processos

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Elisiane%20Quadros-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/elisiane-quadros/)

</div>

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

<div align="center">

Desenvolvido com 💙 por **Elisiane Quadros** — © 2026

*Tornando a web mais inclusiva, um site de cada vez.*

</div>
