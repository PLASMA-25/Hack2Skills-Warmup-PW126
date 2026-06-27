# Cooking To-Do List — PromptWars Warm-up

AI micro-app: describe what you want to cook, get a **breakfast/lunch/dinner plan**, **grocery list**, **substitutions**, and **budget check**.

## Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI + LangGraph + OpenAI (structured Pydantic output)
- **Deploy:** Single Docker container (API serves built frontend)

## Architecture

1. User submits free-text intent + budget
2. **Intent extractor** → structured `ParsedIntent`
3. If required fields missing → **supervisor** asks dynamic question (from Pydantic field descriptions)
4. **Meal agents** (breakfast / lunch / dinner) run for requested slots
5. **Grocery** → **Substitutions** → **Budget** (with retry if over budget)

## Setup

### Environment

```bash
cp .env.example .env
# Set OPENAI_API_KEY in .env
```

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Tests

```bash
cd backend && python -m pytest
cd frontend && npm test
```

## Docker (full stack — one URL)

```bash
docker build -t cooking-todo .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... cooking-todo
```

## Deploy — Cloudflare Pages + backend

Cloudflare Pages hosts the **frontend only**. The Python API must run on a container host (Render recommended) because LangGraph/FastAPI cannot run on Pages.

### Step 1 — Push (done)

Repo: https://github.com/PLASMA-25/Hack2Skills-Warmup-PW126

### Step 2 — Backend on Render (Docker)

1. [Render](https://render.com) → **New Web Service** → connect this repo
2. **Environment:** Docker
3. **Environment variables:**
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL=gpt-4o-mini`
   - `CORS_ORIGINS=https://YOUR-PROJECT.pages.dev,http://localhost:5173`
4. Deploy → copy URL (e.g. `https://cooking-todo.onrender.com`)

### Step 3 — Frontend on Cloudflare Pages

1. [Cloudflare Dashboard](https://dash.cloudflare.com) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Select `PLASMA-25/Hack2Skills-Warmup-PW126`
3. Build settings:

| Setting | Value |
|---------|-------|
| Root directory | `frontend` |
| Build command | `npm run build` |
| Build output | `dist` |

4. **Environment variable (Production):**
   - `VITE_API_BASE_URL` = your Render backend URL (no trailing slash)

5. Deploy → open `https://YOUR-PROJECT.pages.dev`

### Step 4 — Verify

- Frontend loads
- Submit a meal plan → API calls go to Render backend
- If CORS errors: add your exact `*.pages.dev` URL to `CORS_ORIGINS` on Render and redeploy

### All-in-one alternative

Skip Cloudflare and deploy the **Dockerfile only** on Render — one service serves UI + API at a single URL (no `VITE_API_BASE_URL` needed).

## Evaluation priorities

See `.cursor/rules/` — high impact: code quality + problem alignment; medium: security + efficiency; tiebreakers: testing + accessibility.
