import asyncio
from contextlib import asynccontextmanager

from playwright._impl._errors import TargetClosedError
from playwright.async_api import async_playwright

# Flags obrigatórias para o Chromium rodar em container Docker
CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-features=IsolateOrigins,site-per-process",
]

CONTEXT_OPTIONS = {
    "viewport": {"width": 1280, "height": 720},
    "ignore_https_errors": True,
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

_browser = None
_playwright = None
_lock = asyncio.Lock()


def _browser_is_alive() -> bool:
    """Verifica se o processo do navegador singleton está vivo e conectado."""
    return _browser is not None and _browser.is_connected()


async def init_browser():
    """Inicializa o navegador singleton uma única vez na inicialização do servidor."""
    global _browser, _playwright
    if _browser_is_alive():
        return

    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(args=CHROMIUM_ARGS)


async def close_browser():
    """Fecha o navegador singleton no desligamento do servidor."""
    global _browser, _playwright
    if _browser:
        try:
            await _browser.close()
        except Exception:
            pass
        _browser = None
    if _playwright:
        try:
            await _playwright.stop()
        except Exception:
            pass
        _playwright = None


async def _reset_browser():
    """
    Reinicia o navegador se o processo foi morto (ex.: estouro de memória).

    Usa is_connected() como verificação de vida — browser.contexts não serve
    para isso, pois é uma propriedade local que nunca é None nem lança erro,
    mesmo com o navegador morto.

    O double-check dentro do lock evita que requisições concorrentes
    relancem o navegador múltiplas vezes: a primeira reseta, as demais
    encontram o navegador já vivo e retornam.
    """
    global _browser, _playwright
    async with _lock:
        if _browser_is_alive():
            return  # outra requisição já resetou enquanto esperávamos o lock

        await close_browser()
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(args=CHROMIUM_ARGS)


@asynccontextmanager
async def browser_session():
    """
    Fornece uma página temporária a partir do navegador singleton.

    Cada chamada cria um contexto + página leves em vez de iniciar
    um navegador inteiro, economizando ~200MB de memória por requisição.

    Se o processo do navegador morrer entre requisições, ele é
    reiniciado automaticamente antes de criar a nova página.
    """
    if _browser is None:
        raise RuntimeError(
            "Navegador não inicializado. O servidor pode não ter iniciado corretamente."
        )

    try:
        context = await _browser.new_context(**CONTEXT_OPTIONS)
    except TargetClosedError:
        await _reset_browser()
        context = await _browser.new_context(**CONTEXT_OPTIONS)

    page = await context.new_page()
    try:
        yield page
    finally:
        # Se o navegador morreu no meio da inspeção, close() lançaria
        # TargetClosedError e mascararia o erro original da requisição.
        try:
            await page.close()
        except Exception:
            pass
        try:
            await context.close()
        except Exception:
            pass
