import httpx
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from backend.config.settings import get_settings
from contextlib import asynccontextmanager

settings = get_settings()

@asynccontextmanager
async def browser_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            yield page
        finally:
            await browser.close()


# Esta função será usada pelo main.py para abrir o browser uma única vez
async def get_page_for_url(url: str, p):
    browser = await p.chromium.launch()
    # Opcional: Adicione um user-agent para evitar bloqueios
    context = await browser.new_context(user_agent="Mozilla/5.0 (compatible; A11yInspector/2.0)")
    page = await context.new_page()

    await page.goto(
        str(url),
        timeout=settings.request_timeout * 1000,
        wait_until="networkidle"
    )
    return browser, page


# Estratégia rápida — para sites simples sem JavaScript
async def fetch_html_simple(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; A11yInspector/2.0)"
    }
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        response = await client.get(str(url), headers=headers, follow_redirects=True)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")


# Estratégia completa — para sites que precisam de JavaScript
async def fetch_html_rendered(url: str) -> BeautifulSoup:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            page = await browser.new_page()
            await page.goto(
                str(url),
                timeout=settings.request_timeout * 1000,
                wait_until="networkidle"
            )
            html = await page.content()
            return BeautifulSoup(html, "lxml")
        finally:
            await browser.close()


# Porta de entrada — tenta simples primeiro, cai pro Playwright se falhar
async def fetch_html(url: str) -> BeautifulSoup:
    try:
        return await fetch_html_simple(url)
    except Exception:
        return await fetch_html_rendered(url)