# Imagem base com Playwright e Python já configurados
FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app

# Instala dependências Python primeiro (cache de layer)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala apenas o Chromium (já vem na imagem base, garante a versão correta)
RUN playwright install chromium

# Copia o restante do projeto
COPY . .

# Expõe a porta
EXPOSE 8000

# Inicia o servidor com uvicorn
# Usa 0.0.0.0 para aceitar conexões externas (necessário no Railway)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
