# A11y Inspector

**Auditoria de Acessibilidade Digital com Inteligência Artificial**

---

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React_19-TypeScript-3178C6?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![Playwright](https://img.shields.io/badge/Playwright-1.60-45ba4b?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev)
[![Testes](https://img.shields.io/badge/Testes-65%20passing-success?style=flat-square&logo=pytest&logoColor=white)]()
[![Groq](https://img.shields.io/badge/Groq%20Llama-F55036?style=flat-square&logo=groq&logoColor=white)](https://groq.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![Status](https://img.shields.io/badge/Status-MVP%20%E2%80%93%20Demo%20online-2ea44f?style=flat-square)]()

<br/>

> 🔗 **[Acesse a demonstração](https://site-inspector-eq.vercel.app/)** — nenhum cadastro necessário.

<br/>

O **A11y Inspector** é uma ferramenta de auditoria de acessibilidade digital. Ela analisa websites sob demanda, detecta falhas com base nas diretrizes WCAG 2.1 e na Lei Brasileira de Inclusão (LBI), utiliza inteligência artificial para gerar análises estratégicas e produz relatórios PDF prontos para gestores e equipes técnicas.

<br/>

![Painel de resultados da inspeção, exibindo categorias auditadas e botões de exportação de PDF](assets/resultado_inspecao_online.png)

---

## Sobre o Projeto

O A11y Inspector foi construído para resolver um problema específico: automatizar inspeções de acessibilidade digital combinando backend assíncrono, inteligência artificial multimodal e renderização headless — e transformar o resultado em algo útil tanto para engenheiros quanto para gestores.

O backend é escrito em Python com FastAPI, utiliza Playwright para renderizar páginas reais e BeautifulSoup para análise estrutural do HTML. Dois modelos de IA, um por tarefa: um LLM via Groq gera a análise executiva contextualizada por segmento de negócio, e o Gemini realiza a análise multimodal das imagens para sugerir textos alternativos. O frontend é uma SPA em React com TypeScript que renderiza dois tipos de PDF no client-side.

> **Visão futura.** Este é o primeiro módulo do **SiteInspector**, um projeto guarda-chuva que prevê a criação de uma plataforma modular de auditoria web. Os demais módulos (privacidade, segurança, SEO) estão em estágio de planejamento e não estão implementados.

---

## Problema

A acessibilidade digital deixou de ser apenas uma boa prática. No Brasil, a Lei Brasileira de Inclusão (Lei nº 13.146/2015) estabelece requisitos de inclusão digital, e o descumprimento pode gerar riscos legais, como notificações do Ministério Público, ações civis públicas e outras medidas judiciais.

Apesar desse cenário, muitas organizações ainda dependem de auditorias manuais, ferramentas limitadas ou relatórios excessivamente técnicos, dificultando a identificação, priorização e correção das barreiras de acessibilidade.

O mercado carece de ferramentas que:

- Realizem inspeções automatizadas e sob demanda.
- Traduzam problemas técnicos em informações úteis para gestores e compliance.
- Gerem relatórios técnicos e executivos prontos para tomada de decisão.
- Adaptem recomendações ao contexto de diferentes segmentos, como e-commerce, SaaS e sites institucionais.

---

## Solução

O A11y Inspector resolve esse problema combinando três camadas complementares:

1. **Inspeção automatizada.** Um motor de auditoria percorre o HTML do site alvo e identifica falhas estruturais — imagens sem descrição, formulários sem rótulo, hierarquia de títulos quebrada, links vagos, botões inacessíveis, landmarks ausentes e problemas de navegação por teclado. A análise de contraste de cores é feita sobre o DOM real renderizado via Playwright.

2. **Inteligência artificial contextual.** A ferramenta consome dois modelos de IA, um por tarefa: o Gemini gera descrições alternativas de imagens via análise multimodal, e um LLM via Groq produz relatórios executivos estratégicos adaptados ao segmento de negócio detectado automaticamente.

3. **Relatórios duplos em PDF.** Cada inspeção gera dois documentos: um Relatório Executivo para gestores e compliance, com análise de risco legal e impacto de negócio; e um Checklist Técnico para desenvolvedores, com ocorrências, snippets HTML e orientações de correção.

---

## Diferenciais

### Pipeline assíncrono com controle de concorrência

Operações de I/O bloqueantes — scraping, download de páginas, chamadas às APIs de IA — são gerenciadas com `asyncio`, `asyncio.Semaphore` e `asyncio.wait_for`. O loop de eventos do FastAPI nunca é bloqueado, garantindo que o backend mantenha capacidade de resposta sob carga.

### Orquestração multi-provedor de IA

Dois modelos especializados, um por tarefa: o relatório executivo é gerado por LLM via Groq, com prompts adaptados ao segmento do site e guardrails contra fabricação de números; as descrições de imagem vêm do Gemini, consumido pela API nativa, com download validado que filtra pixels de rastreamento antes de gastar cota. Os modelos são parametrizados por variável de ambiente, permitindo troca sem deploy.

| Modelo | Provedor | Função |
|---|---|---|
| `llama-3.3-70b-versatile` | Groq | Geração do relatório executivo estratégico, contextualizado por segmento de negócio |
| `gemini-2.5-flash-lite` | Google (API nativa) | Geração de texto alternativo (`alt`) para imagens, via análise multimodal |

A detecção do segmento de negócio é feita por regex em Python puro — sem depender de IA para essa classificação, o que mantém a etapa rápida e determinística.

### Renderização real com Playwright

A análise de contraste de cores e o parsing de aplicações single-page (React, Vue, Angular) utilizam o Playwright em modo headless. O DOM analisado é o DOM real renderizado pelo navegador, não o HTML estático do servidor. Uma sessão única é reutilizada durante toda a inspeção, evitando a abertura e fechamento repetidos do navegador.

### Validação e serialização com Pydantic

A hierarquia de modelos (`BaseIssue` → tipos especializados como `ImageAccessibilityIssue`) com tipagem combinatória (`Union`) garante que propriedades específicas de cada tipo de falha — inclusive metadados gerados por IA — sejam preservadas durante a serialização JSON, sem perda de dados.

### Roadmap de prioridades determinístico

As falhas são classificadas em três níveis de prioridade por um algoritmo em Python puro:

- **P1 — Crítico.** Risco legal direto ou bloqueio total de uso.
- **P2 — Alto.** Impacto em conversão e experiência do usuário.
- **P3 — Médio.** Impacto em estrutura, SEO e semântica.

---

## Funcionalidades

| Funcionalidade | Critério WCAG |
|---|---|
| **Auditoria de Imagens** — detecta `alt` ausente e gera descrição automática via IA multimodal | 1.1.1 |
| **Validação de Formulários** — campos sem `label`, `aria-label`, `aria-labelledby` ou `title` | 1.3.1 |
| **Hierarquia de Títulos** — verifica saltos de nível, múltiplos H1 e H1 ausente | 1.3.1 |
| **Links com Texto Vago** — detecta âncoras genéricas como "clique aqui" e "saiba mais" | 2.4.4 |
| **Botões Inacessíveis** — botões sem texto ou `aria-label`, incluindo elementos com `role="button"` | 4.1.2 |
| **Navegação por Teclado** — detecta `tabindex` positivo e elementos interativos não focáveis | 2.1.1 |
| **Landmarks Semânticos** — verifica presença de `<main>`, `<nav>`, `<header>` e `<footer>` | 1.3.6 |
| **Contraste de Cores** — análise dinâmica via Playwright sobre o DOM renderizado | 1.4.3 |
| **Roadmap de Prioridades** — classificação P1/P2/P3 com justificativa de impacto | — |
| **Relatório Executivo com IA** — análise estratégica gerada por segmento de negócio | — |
| **Checklist Técnico em PDF** — ocorrências, snippets HTML e orientações de correção | — |

---

## Principais Recursos em Ação

### Card Detalhado com Sugestão de IA

![Card detalhado exibindo inconformidade com sugestão de texto alternativo gerada por IA](assets/card_detalhado.png)

<br/>

### Relatórios Gerados Automaticamente

Os PDFs são gerados no client-side via `@react-pdf/renderer` ao final de cada inspeção.

#### 1️⃣ Relatório Executivo

| Resumo da Inspeção | Análise Estratégica por IA | Roadmap de Prioridades |
|---|---|---|
| ![Primeira página do relatório executivo com diagnóstico de exposição legal](assets/resultado_inspecao.png) | ![Página de análise estratégica com recomendações por segmento](assets/diagnostico_ia.png) | ![Roadmap de prioridades P1, P2 e P3 organizado por criticidade](assets/roadmaps_prioridades.png) |

Destinado a gestores, liderança e compliance.

<br/>

#### 2️⃣ Checklist Técnico

<img src="assets/relatorio_tecnico.png" width="320" alt="Checklist técnico com ocorrências, snippets HTML e orientações de correção" />

Destinado à equipe de desenvolvimento, contendo ocorrências detalhadas, snippets HTML, critérios WCAG e orientações de correção.

---

## Stack Tecnológica

### Backend

| Tecnologia | Por que foi escolhida |
|---|---|
| **Python 3.10+** | Ecossistema maduro para IA/ML, automação e processamento de dados. |
| **FastAPI 0.136** | Performance assíncrona nativa com `async/await` e validação via Pydantic. |
| **Playwright 1.60** | Renderização headless confiável para análise de contraste e parsing de SPAs. |
| **BeautifulSoup4 + lxml** | Parsing de HTML rápido e tolerante a erros de marcação. |
| **Groq SDK** | API de LLMs com latência reduzida (inferência em hardware LPU dedicado). |
| **Pydantic + Pydantic Settings** | Serialização validada e configuração via `.env` com cache LRU. |
| **Uvicorn 0.48** | Servidor ASGI de alta performance, padrão para aplicações FastAPI. |
| **httpx** | Cliente HTTP assíncrono com keep-alive e timeouts configuráveis. |

### Frontend

| Tecnologia | Por que foi escolhida |
|---|---|
| **React 19 + TypeScript** | Componentização com tipagem estática. |
| **Tailwind CSS 3.4** | Estilização utilitária e responsiva sem arquivos CSS avulsos. |
| **Vite 6.3** | Build tool com hot-reload instantâneo. |
| **@react-pdf/renderer** | Geração de PDF no client-side sem servidor dedicado. |

### Infraestrutura

| Tecnologia | Por que foi escolhida |
|---|---|
| **Docker** | Imagem oficial `playwright/python` com todas as dependências de sistema. |
| **Render** | Deploy do backend containerizado com suporte nativo a Docker. |
| **Vercel** | Deploy do frontend SPA React com CDN global. |

---

## Arquitetura

A aplicação segue uma arquitetura de duas camadas independentes que se comunicam via API REST.

### Backend (FastAPI)

O backend implementa um pipeline de três estágios:

1. **Coleta.** O motor recebe uma URL, dispara o Playwright em modo headless, carrega a página alvo e executa scripts de extração diretamente no DOM renderizado. Um `asyncio.Semaphore` limita a concorrência e um timeout configurável evita travamentos.

2. **Análise.** O HTML coletado é processado pelo BeautifulSoup para auditoria estrutural (imagens, formulários, headings, links, botões, landmarks, foco). Paralelamente, os dados de cores extraídos pelo Playwright são processados em Python puro para cálculo de contraste segundo a fórmula WCAG 2.1.

3. **Síntese.** Os resultados são enriquecidos com IA (descrição de imagens e relatório executivo) e organizados em um roadmap de prioridades P1/P2/P3. O frontend recebe o payload completo e renderiza os PDFs no client-side.

### Frontend (React SPA)

O frontend é uma aplicação de página única que consome a API do backend. O fluxo de uso é:

- O usuário insere uma URL.
- O frontend envia a URL para o endpoint de inspeção.
- Durante o processamento, um componente de loading exibe o progresso.
- Ao final, os resultados são exibidos em cards categorizados, com opção de baixar os PDFs.

---

## Estrutura do Projeto

```
A11yInspector/
│
├── Dockerfile                          # Imagem Docker com Playwright + Python
├── pyproject.toml                      # Dependências e metadados do projeto Python
├── run.py                              # Entrypoint que carrega .env e inicia Uvicorn
├── .env.example                        # Template de variáveis de ambiente
├── pytest.ini                          # Configuração do pytest
│
├── assets/                             # Imagens de demonstração do projeto
│
├── backend/
│   ├── __init__.py
│   ├── main.py                         # Endpoints FastAPI e orquestração do pipeline
│   ├── requirements.txt
│   ├── config/
│   │   └── settings.py                 # Configurações via Pydantic Settings
│   ├── models/
│   │   └── schemas.py                  # Contratos de dados com herança e tipagem combinatória
│   ├── scanner/
│   │   └── core.py                     # Motor de auditoria estrutural
│   └── utils/
│       ├── ai_assistant.py             # Pipeline de IA: relatório via Groq + descrições via Gemini
│       ├── contrast.py                 # Análise de contraste via Playwright
│       ├── color_parser.py             # Parsing de cores CSS
│       ├── html_fetcher.py             # Gerenciador de sessão única do Playwright
│       └── priority.py                 # Gerador de roadmap P1/P2/P3
│
├── frontend/
│   ├── index.html                      # Entrypoint HTML do Vite
│   ├── package.json                    # Dependências Node.js
│   ├── vite.config.ts                  # Configuração do Vite
│   ├── vercel.json                     # Configuração de deploy na Vercel
│   ├── postcss.config.js               # Configuração do PostCSS/Tailwind
│   ├── tailwind.config.js              # Configuração do Tailwind CSS
│   ├── tsconfig.json                   # Configuração base do TypeScript
│   ├── tsconfig.app.json               # Configuração TS para o app
│   ├── tsconfig.node.json              # Configuração TS para Node
│   ├── eslint.config.js                # Configuração do ESLint
│   └── src/
│       ├── main.tsx                    # Ponto de entrada React
│       ├── App.tsx                     # Componente raiz com roteamento
│       ├── App.css                     # Estilos globais do App
│       ├── index.css                   # Estilos base/Tailwind
│       ├── vite-env.d.ts               # Tipos Vite
│       ├── assets/                     # Assets estáticos (PDFs, imagens)
│       ├── components/
│       │   ├── UrlForm.tsx
│       │   ├── InspectorLoader.tsx
│       │   ├── ResultCard.tsx
│       │   ├── ReportPDF.tsx
│       │   ├── ExecutiveReportPDF.tsx
│       │   ├── TechnicalReportPDF.tsx
│       │   └── __tests__/              # Testes dos componentes
│       ├── interfaces/
│       │   ├── AccessibilityResults.ts
│       │   ├── CheckRequest.ts
│       │   ├── ResultItem.ts
│       │   └── ResultContrast.ts
│       ├── services/
│       │   └── api.ts
│       └── test/
│           └── setup.ts                # Setup de testes
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_scanner_core.py
    ├── test_contrast.py
    ├── test_color_parser.py
    ├── test_business_segment.py
    └── test_priority.py
```

---

## Testes

| Arquivo | Cobertura |
|---|---|
| `test_scanner_core.py` | Motor de auditoria — imagens, formulários, headings, links, botões, landmarks e navegação por teclado |
| `test_contrast.py` | Cálculo de contraste WCAG 1.4.3 |
| `test_color_parser.py` | Parsing de cores CSS para tuplas RGB |
| `test_business_segment.py` | Detecção de segmento de negócio (e-commerce, SaaS, corporativo) |
| `test_priority.py` | Geração e ordenação do roadmap P1/P2/P3 |

```bash
python -m pytest tests/ -v
# 65 passed in ~1.4s
```

---

## Roadmap

Os itens abaixo representam a visão de evolução do projeto. Apenas o primeiro está implementado.

- **A11y Inspector.** MVP publicado.
- **SiteInspector — Landing Page.** Em desenvolvimento.
- **Dashboard com histórico de inspeções.** Planejado.
- **Autenticação de usuários (JWT).** Planejado.
- **Módulo Privacy Inspector.** Planejado.
- **Módulo Security Inspector.** Planejado.
- **Módulo SEO Inspector.** Planejado.
- **API pública com rate limiting.** Planejado.
- **Monitoramento contínuo com alertas.** Planejado.

---

## Licença

Este projeto é proprietário. O código-fonte está disponível publicamente para avaliação técnica, mas não pode ser reutilizado, modificado ou redistribuído sem autorização expressa da autora.

© 2026 Elisiane Quadros. Todos os direitos reservados.

---

## Contato

**Elisiane Quadros**

Desenvolvedora Python | Full Stack | AI Engineer Júnior | LLMs, RAG, LangGraph | FastAPI

[LinkedIn](https://www.linkedin.com/in/elisiane-quadros/) &nbsp;·&nbsp; [GitHub](https://github.com/elisiane-quadros)
