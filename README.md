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

## Docker

```bash
docker build -t cooking-todo .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... cooking-todo
```

## Evaluation priorities

See `.cursor/rules/` — high impact: code quality + problem alignment; medium: security + efficiency; tiebreakers: testing + accessibility.
