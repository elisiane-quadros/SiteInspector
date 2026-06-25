# 🚀 Guia de Deploy — SiteInspector

Guia passo a passo para colocar o SiteInspector no ar com **Railway (backend)** + **Vercel (frontend)**.

---

## 📦 1. Backend — Railway

### 1.1. Pré-requisitos

- Conta no [Railway](https://railway.app) (login com GitHub)
- Repositório no GitHub com o projeto

### 1.2. Fazer o push para o GitHub

```bash
git add .
git commit -m "chore: configura arquivos para deploy Railway + Vercel"
git push origin develop
```

### 1.3. Criar o projeto no Railway

1. Acesse [railway.app](https://railway.app) e clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Escolha o repositório `SiteInspector`
4. O Railway vai detectar automaticamente o `Dockerfile` e começar o build

### 1.4. Configurar variáveis de ambiente no Railway

No painel do Railway, vá em **Variables** e adicione:

| Variável | Valor | Observação |
|----------|-------|------------|
| `GROQ_API_KEY` | `sua_chave_groq_aqui` | Obrigatória — obtida em https://console.groq.com |
| `ALLOWED_ORIGINS` | `https://seu-projeto.vercel.app` | URL do frontend após deploy na Vercel |
| `APP_ENV` | `production` | Ambiente de produção |
| `REQUEST_TIMEOUT` | `30` | Timeout padrão |
| `MAX_ELEMENTS` | `200` | Limite de elementos |

> ⚠️ **Importante:** A variável `ALLOWED_ORIGINS` precisa ser atualizada **depois** que o frontend estiver no ar.

### 1.5. Obter a URL do backend

Após o deploy, o Railway vai gerar uma URL como:
```
https://siteinspector-production.up.railway.app
```

Anote essa URL — você vai precisar para configurar o frontend.

---

## 🎨 2. Frontend — Vercel

### 2.1. Pré-requisitos

- Conta na [Vercel](https://vercel.com) (login com GitHub)

### 2.2. Configurar a URL da API

Edite o arquivo `frontend/.env.production`:

```env
# frontend/.env.production
VITE_API_URL=https://seu-backend.up.railway.app/api
```

Substitua pela URL do seu backend no Railway.

### 2.3. Fazer o commit e push

```bash
git add frontend/.env.production
git commit -m "chore: configura URL da API para produção"
git push origin develop
```

### 2.4. Deploy na Vercel

1. Acesse [vercel.com](https://vercel.com) e clique em **"Add New" → "Project"**
2. Importe o repositório `SiteInspector`
3. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend` ⬅️ **IMPORTANTE!**
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Clique em **"Deploy"**

### 2.5. (Alternativa) Deploy via CLI da Vercel

```bash
cd frontend
npx vercel --prod
```

### 2.6. Obter a URL do frontend

A Vercel vai gerar uma URL como:
```
https://siteinspector.vercel.app
```

---

## 🔗 3. Finalizar a integração

Agora que ambos estão no ar:

1. **Copie a URL do frontend** (ex: `https://siteinspector.vercel.app`)
2. **No Railway**, atualize a variável:
   - `ALLOWED_ORIGINS=https://siteinspector.vercel.app`
3. **Re-deploy** o backend no Railway (ou ele reinicia automaticamente)

---

## ✅ 4. Verificar se está funcionando

### Testar o backend

```bash
curl https://seu-backend.up.railway.app/
```

Resposta esperada:
```json
{
  "status": "online",
  "app": "A11y Inspector API",
  "version": "2.0.0",
  "docs": "/docs"
}
```

### Testar o frontend

Acesse a URL do frontend no navegador e faça uma inspeção de teste.

---

## 🐳 5. Estrutura de arquivos para deploy

```
SiteInspector/
├── Dockerfile              # ✅ Já configurado
├── railway.json            # ✅ Configuração do Railway
├── runtime.txt             # ✅ Versão do Python
├── .env.example            # ✅ Template de variáveis
├── backend/
│   └── main.py             # ✅ FastAPI configurado
└── frontend/
    ├── vercel.json         # ✅ Configuração da Vercel
    └── .env.production     # ⚠️  Precisa atualizar a URL
```

---

## 🔄 6. Atualizações futuras

Sempre que fizer alterações no código:

```bash
git add .
git commit -m "descrição das alterações"
git push origin develop
```

- **Railway:** Faz deploy automático ao detectar push no branch `develop`
- **Vercel:** Faz deploy automático ao detectar push no branch `develop`

---

## 🆘 7. Troubleshooting

### Backend não sobe no Railway

Verifique os logs no painel do Railway:
- Erro de `GROQ_API_KEY` ausente → Adicione a variável
- Erro de Playwright → O Dockerfile já instala o Chromium
- Timeout no build → O Dockerfile pode levar 5-10 minutos na primeira vez

### Frontend não conecta ao backend

- Verifique se `VITE_API_URL` está correta no `.env.production`
- Verifique se `ALLOWED_ORIGINS` no Railway inclui a URL do frontend
- Verifique o CORS no navegador (console do dev tools)

### Erro de CORS

No backend, a variável `ALLOWED_ORIGINS` aceita múltiplas URLs separadas por vírgula:
```
ALLOWED_ORIGINS=http://localhost:5173,https://siteinspector.vercel.app
```

---

<div align="center">

Feito com 💙 por **Elisiane Quadros**

</div>
