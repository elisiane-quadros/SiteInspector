import asyncio
import sys
import uvicorn

from pathlib import Path
from dotenv import load_dotenv

# Força o Python a buscar o arquivo .env exatamente na raiz do projeto
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


if __name__ == "__main__":
    # A ProactorEventLoopPolicy só existe no Windows e é necessária para o
    # subprocesso do Playwright. Em Linux/macOS o loop padrão já funciona.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )