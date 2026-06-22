from contextlib import asynccontextmanager
from playwright.async_api import async_playwright


@asynccontextmanager
async def browser_session():
    """
    Abre um Chromium headless uma única vez e entrega a `page` pronta para uso.
    O bloco `finally` garante o fechamento do navegador mesmo se ocorrer erro
    durante a análise — evitando processos órfãos do Playwright.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            yield page
        finally:
            await browser.close()
