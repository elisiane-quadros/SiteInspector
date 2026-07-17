from contextlib import asynccontextmanager
from playwright.async_api import async_playwright


# Flags essenciais para rodar Chromium em container Docker com memória limitada:
#   --no-sandbox + --disable-setuid-sandbox  → necessários em ambiente Docker
#   --disable-dev-shm-usage                   → usa /tmp ao invés de /dev/shm (64MB no Docker)
#   --disable-gpu                             → servidor não tem GPU
#   --single-process                          → elimina processos filhos (GPU, renderer, zygote)
#   --no-zygote                               → desliga o processo zygote (~30MB)
#   --disable-extensions                      → sem extensões desnecessárias
#   --disable-features=IsolateOrigins,...     → NÃO cria um processo por origem carregada
CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--single-process",
    "--no-zygote",
    "--disable-extensions",
    "--disable-features=IsolateOrigins,site-per-process",
]

_browser = None      # singleton: um navegador para toda a vida do servidor
_playwright = None    # instância do Playwright (vive junto com o navegador)


async def init_browser():
    """
    Inicializa o navegador UMA ÚNICA VEZ (chamado no startup do servidor).
    Sempre seguro chamar múltiplas vezes — ignora se já estiver rodando.
    """
    global _browser, _playwright
    if _browser is not None:
        return  # já inicializado

    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(
        args=CHROMIUM_ARGS,
    )


async def close_browser():
    """
    Fecha o navegador UMA ÚNICA VEZ (chamado no shutdown do servidor).
    Sempre seguro chamar múltiplas vezes — ignora se já estiver fechado.
    """
    global _browser, _playwright
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None


@asynccontextmanager
async def browser_session():
    """
    Abre uma NOVA ABA (page) no navegador singleton já em execução.
    
    DIFERENÇA CRÍTICA (vs. versão anterior):
    Antes: um navegador INTEIRO era iniciado e fechado a cada requisição.
    Agora: o navegador já está rodando — só criamos/limpamos uma aba leve.
    
    Isso reduz o consumo de memória de ~300-400MB por requisição
    para ~80-120MB estáveis no servidor inteiro.
    """
    if _browser is None:
        raise RuntimeError(
            "Navegador não inicializado. Certifique-se de que o servidor "
            "iniciou corretamente (init_browser é chamado no lifespan)."
        )

    context = await _browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    )
    page = await context.new_page()
    try:
        yield page
    finally:
        await page.close()
        await context.close()
