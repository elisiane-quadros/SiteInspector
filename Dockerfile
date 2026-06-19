# Imagem base com Playwright e Python já configurados
# Evita instalar dependências do sistema manualmente
FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app

# Instala dependências Python primeiro (cache de layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala apenas o Chromium (já vem na imagem base, garante a versão correta)
RUN playwright install chromium

# Copia o restante do projeto
COPY . .

# Porta exposta pelo FastAPI
EXPOSE 8000

# Inicia o servidor
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]