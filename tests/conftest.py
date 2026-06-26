"""
Configuração global dos testes do backend.

Adiciona a raiz do projeto ao sys.path para que os imports
absolutos (ex: `from backend.scanner.core import ...`)
funcionem corretamente ao rodar `pytest` de qualquer diretório.
"""
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path do Python
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
