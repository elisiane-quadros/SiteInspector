# SiteInspector

**Plataforma Inteligente de Auditoria para Websites**

---

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React_19-TypeScript-3178C6?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![Playwright](https://img.shields.io/badge/Playwright-1.60-45ba4b?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev)
[![Testes](https://img.shields.io/badge/Testes-65%20passing-success?style=flat-square&logo=pytest&logoColor=white)]()
[![Groq](https://img.shields.io/badge/Groq%20Llama-F55036?style=flat-square&logo=groq&logoColor=white)](https://groq.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![Licence](https://img.shields.io/badge/Licen%C3%A7a-Propriet%C3%A1ria-6B21A8?style=flat-square)]()

<br/>

> 🔗 **[Acesse a demonstração](https://site-inspector-eq.vercel.app/)** — nenhum cadastro necessário.

<br/>

<br/>

**SiteInspector** é uma plataforma em desenvolvimento para auditoria automatizada de websites. Ela será composta por módulos especializados que inspecionam diferentes aspectos de um site — acessibilidade, privacidade, segurança, SEO — de forma isolada ou combinada.

O **A11y Inspector** é o primeiro módulo disponível. Ele realiza inspeções sob demanda de acessibilidade digital com base nas diretrizes WCAG 2.1 e na Lei Brasileira de Inclusão (LBI), combinando automação com navegador headless, parsing de HTML e inteligência artificial para gerar relatórios PDF estratégicos e técnicos.

<br/>

![Painel de resultados da inspeção, exibindo categorias auditadas e botões de exportação de PDF](assets/resultado_inspecao_online.png)

---

## Sobre o SiteInspector

O SiteInspector nasceu como um projeto de demonstração de engenharia backend Python com foco em IA e automação. Durante o desenvolvimento, ficou claro que o modelo de inspeção automatizada poderia se estender para outras áreas além de acessibilidade.

A visão da plataforma é oferecer um conjunto de módulos especializados que compartilham a mesma infraestrutura de back-end, sessão de navegador headless e pipeline de IA, permitindo que cada inspeção seja realizada de forma isolada ou composta.

Atualmente, a plataforma conta com o módulo de acessibilidade implementado. Os demais módulos fazem parte do roadmap de evolução do produto.

---

## Problema

A acessibilidade digital deixou de ser apenas uma boa prática. No Brasil, a Lei Brasileira de Inclusão (Lei nº 13.146/2015) estabelece requisitos de inclusão digital, e o descumprimento pode gerar riscos legais, como notificações do Ministério Público, ações civis públicas e outras medidas judiciais.

Apesar desse cenário, muitas organizações ainda dependem de auditorias manuais, ferramentas limitadas ou relatórios excessivamente técnicos, dificultando a identificação, priorização e correção das barreiras de acessibilidade.

O mercado carece de ferramentas que:

- Realizem inspeções automatizadas e sob demanda.
- Traduzam problemas técnicos em informações úteis para gestores e equipes de compliance.
- Gerem relatórios técnicos e executivos prontos para tomada de decisão.
- Adaptem recomendações ao contexto de diferentes segmentos, como e-commerce, SaaS e sites institucionais.
---

## Solução

O A11y Inspector resolve esse problema combinando três camadas complementares:

1. **Inspeção automatizada.** Um motor de auditoria percorre o HTML do site alvo e identifica falhas estruturais — imagens sem descrição, formulários sem rótulo, hierarquia de títulos quebrada, links vagos, botões inacessíveis, landmarks ausentes e problemas de navegação por teclado. A análise de contraste de cores é feita sobre o DOM real renderizado via Playwright.

2. **Inteligência artificial contextual.** A plataforma consome dois modelos distintos da API Groq: um para gerar descrições alternativas de imagens via análise multimodal, e outro para produzir relatórios executivos estratégicos adaptados ao segmento de negócio detectado automaticamente (e-commerce, SaaS ou corporativo).

3. **Relatórios duplos em PDF.** Cada inspeção gera dois documentos: um Relatório Executivo para gestores e compliance, com análise de risco legal e impacto de negócio; e um Checklist Técnico para desenvolvedores, com ocorrências, snippets HTML e orientações de correção.

---

## Diferenciais

### Pipeline assíncrono com controle de concorrência

Operações de I/O bloqueantes — scraping, download de páginas, chamadas à API Groq — são gerenciadas com `asyncio`, `asyncio.Semaphore` e `asyncio.wait_for`. O loop de eventos do FastAPI nunca é bloqueado, garantindo que o backend mantenha capacidade de resposta sob carga.

### Integração com LLMs via Groq

Dois modelos especializados operam em paralelo:

| Modelo | Finalidade |
|---|---|
| `llama-3.3-70b-versatile` | Geração do relatório executivo estratégico, contextualizado por segmento de negócio |
| `meta-llama/llama-4-scout-17b-16e-instruct` | Geração de texto alternativo (`alt`) para imagens, via análise multimodal |

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

## Módulos da Plataforma

| Módulo | Status |
|---|---|
| **A11y Inspector** | Disponível |
| Privacy Inspector | Planejado |
| Security Inspector | Planejado |
| SEO Inspector | Planejado |

---

## Funcionalidades do A11y Inspector

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

## Stack Tecnológica

A escolha de cada tecnologia considera o cenário atual e a evolução prevista para a plataforma.

### Backend

| Tecnologia | Por que foi escolhida |
|---|---|
| **Python 3.11+** | Ecossistema maduro para IA/ML, automação e processamento de dados. Tipagem gradual com suporte a `Optional` e `Union` do `typing` permite código expressivo e seguro. |
| **FastAPI 0.136** | Performance assíncrona nativa com `async/await`, validação automática via Pydantic e geração de documentação OpenAPI interativa. Essencial para operações de I/O intensivas como scraping e chamadas de API. |
| **Playwright 1.60** | Única ferramenta que oferece renderização headless confiável com suporte multi-navegador e injeção de JavaScript arbitrário no DOM real. Necessário para análise de contraste e parsing de SPAs. |
| **BeautifulSoup4 + lxml** | Parsing de HTML rápido e tolerante a erros de marcação. Mais leve que Playwright para análise estrutural onde o DOM renderizado não é necessário. |
| **Groq SDK** | API de LLMs com latência significativamente menor que concorrentes (inferência em hardware dedicado LPU). Viabiliza a geração de relatórios em segundos, não minutos. |
| **Pydantic + Pydantic Settings** | Serialização com validação de tipos em tempo de execução. A camada `BaseSettings` gerencia configuração via `.env` com cache LRU, eliminando arquivos de configuração manuais. |
| **Uvicorn 0.48** | Servidor ASGI de alto desempenho, necessário para servir aplicações FastAsyncIO. |
| **httpx** | Cliente HTTP assíncrono com suporte a conexões keep-alive e timeouts configuráveis. |

### Frontend

| Tecnologia | Por que foi escolhida |
|---|---|
| **React 19 + TypeScript** | Componentização com tipagem estática reduz erros em tempo de desenvolvimento. O ecossistema maduro de bibliotecas (Axios, react-pdf) acelera a implementação de features como download de PDF e consumo de API. |
| **Tailwind CSS 3.4** | Estilização utilitária que elimina a necessidade de arquivos CSS avulsos. Responsivo por padrão, o que facilita a adaptação futura para dashboard e histórico. |
| **Vite 6.3** | Build tool com hot-reload instantâneo e bundler otimizado via Rollup. Substitui Webpack com configuração mínima. |
| **@react-pdf/renderer** | Geração de PDF no client-side sem necessidade de servidor dedicado. Documentos renderizados no navegador evitam custos de processamento no backend. |

### Infraestrutura

| Tecnologia | Por que foi escolhida |
|---|---|
| **Docker** | A imagem `mcr.microsoft.com/playwright/python` já inclui Python, navegador Chromium e todas as dependências de sistema necessárias. Elimina conflitos de ambiente e simplifica o deploy em qualquer plataforma de container. |
| **Render** | Plataforma de deploy com suporte nativo a Docker. Utilizada para hospedar o backend com Playwright em ambiente Linux, garantindo compatibilidade com as dependências de sistema do navegador headless. |
| **Vercel** | Deploy otimizado para SPAs React/Vite com preview automático por branch e CDN global. |

---

## Arquitetura

A aplicação segue uma arquitetura de duas camadas independentes que se comunicam via API REST.

### Backend (FastAPI)

O backend implementa um pipeline de três estágios:

1. **Coleta.** O motor recebe uma URL, dispara o Playwright em modo headless, carrega a página alvo e executa scripts de extração diretamente no DOM renderizado. Um `asyncio.Semaphore` limita a concorrência e um timeout configurável evita travamentos.

2. **Análise.** O HTML coletado é processado pelo BeautifulSoup para auditoria estrutural (imagens, formulários, headings, links, botões, landmarks, foco). Paralelamente, os dados de cores extraídos pelo Playwright são processados em Python puro para cálculo de contraste segundo a fórmula WCAG 2.1.

3. **Geração de valor.** Os resultados são enriquecidos com IA (descrição de imagens e relatório executivo via Groq) e organizados em um roadmap de prioridades P1/P2/P3. O frontend recebe o payload completo e renderiza os PDFs no client-side.

### Frontend (React SPA)

O frontend é uma aplicação de página única que consome a API do backend. O fluxo de uso é:

- O usuário insere uma URL.
- O frontend envia a URL para o endpoint de inspeção.
- Durante o processamento, um componente de loading exibe o progresso.
- Ao final, os resultados são exibidos em cards categorizados, com opção de baixar os PDFs.

---

## Estrutura do Projeto

```
SiteInspector/
│
├── Dockerfile                          # Imagem Docker com Playwright + Python
├── railway.json                        # Configuração de deploy no Railway
├── runtime.txt                         # Versão do Python (3.11)
├── run.py                              # Entrypoint que carrega .env e inicia Uvicorn
├── .env.example                        # Template de variáveis de ambiente
├── pytest.ini                          # Configuração do pytest
│
├── backend/
│   ├── __init__.py
│   ├── main.py                         # Endpoints FastAPI e orquestração do pipeline
│   ├── requirements.txt                # Dependências Python
│   ├── config/
│   │   └── settings.py                 # Configurações gerenciadas por Pydantic Settings
│   ├── models/
│   │   └── schemas.py                  # Contratos de dados com herança e tipagem combinatória
│   ├── scanner/
│   │   └── core.py                     # Motor de auditoria estrutural (imagens, forms, etc.)
│   └── utils/
│       ├── ai_assistant.py             # Pipeline Groq para relatório e descrição de imagens
│       ├── contrast.py                 # Análise de contraste via Playwright
│       ├── color_parser.py             # Parsing de cores CSS para tuplas RGB
│       ├── html_fetcher.py             # Gerenciador de sessão única do Playwright
│       └── priority.py                 # Gerador de roadmap de prioridades (P1/P2/P3)
│
├── frontend/
│   ├── vercel.json                     # Configuração de deploy na Vercel
│   ├── .env.production                 # Variáveis de ambiente de produção
│   ├── vite.config.ts                  # Configuração do Vite + Vitest
│   ├── tsconfig.json                   # TypeScript
│   └── src/
│       ├── App.tsx                     # Componente raiz
│       ├── components/
│       │   ├── UrlForm.tsx             # Formulário de entrada da URL
│       │   ├── InspectorLoader.tsx     # Loader durante a inspeção
│       │   ├── ResultCard.tsx          # Card de resultado com modal de detalhes
│       │   ├── ExecutiveReportPDF.tsx  # PDF para gestão e compliance
│       │   └── TechnicalReportPDF.tsx  # PDF para engenharia e TI
│       ├── interfaces/
│       │   ├── AccessibilityResults.ts # Tipo principal do resultado da inspeção
│       │   ├── ResultItem.ts           # Tipo de item individual de falha
│       │   └── ResultContrast.ts       # Tipo de item de falha de contraste
│       └── services/
│           └── api.ts                  # Cliente Axios configurado
│
└── tests/
    ├── __init__.py
    ├── conftest.py                     # Configuração global de path para imports
    ├── test_scanner_core.py            # Testes do motor de auditoria (BeautifulSoup)
    ├── test_contrast.py                # Testes de cálculo de contraste WCAG
    ├── test_color_parser.py            # Testes de parsing de cores CSS
    ├── test_business_segment.py        # Testes de detecção de segmento de negócio
    └── test_priority.py                # Testes de geração do roadmap P1/P2/P3
```

---
## Testes

A cobertura de testes cobre as camadas críticas do backend — motor de auditoria, parsing de cores, cálculo de contraste, detecção de segmento de negócio e geração do roadmap de prioridades.

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

- **A11y Inspector.** Disponível.
- **Landing Page do SiteInspector.** Em desenvolvimento.
- **Dashboard com histórico de inspeções.** Planejado.
- **Autenticação de usuários (JWT).** Planejado.
- **Módulo Privacy Inspector.** Planejado.
- **Módulo Security Inspector.** Planejado.
- **Módulo SEO Inspector.** Planejado.
- **API pública com rate limiting.** Planejado.
- **Monitoramento contínuo com alertas.** Planejado.

---

## Licença

Este projeto é proprietário. O código-fonte está disponível publicamente para avaliação técnica, mas não pode ser reutilizado, modificado ou redistribuído sem autorização expressa da autora. O SiteInspector está em desenvolvimento ativo como produto SaaS.

© 2026 Elisiane Quadros. Todos os direitos reservados.

---

## Contato

**Elisiane Quadros**

Desenvolvedora Backend Python | Inteligência Artificial e Automação

[LinkedIn](https://www.linkedin.com/in/elisiane-quadros/) &nbsp;·&nbsp; [GitHub](https://github.com/elisiane-quadros)
