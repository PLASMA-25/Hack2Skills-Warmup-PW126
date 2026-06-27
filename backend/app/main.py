import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import health, plan

logger = logging.getLogger(__name__)

app = FastAPI(title="PromptWars API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(plan.router)

# Docker: /app/frontend/dist | Local dev from backend/: ../frontend/dist
_dist_candidates = [
    Path(__file__).resolve().parents[2] / "frontend" / "dist",
    Path(__file__).resolve().parents[3] / "frontend" / "dist",
]
dist_path = next((p for p in _dist_candidates if p.is_dir()), _dist_candidates[0])

if dist_path.is_dir():
    logger.info("Serving frontend from %s", dist_path)
    app.mount("/", StaticFiles(directory=str(dist_path), html=True), name="spa")
else:
    logger.warning("Frontend dist not found at %s", dist_path)

    @app.get("/")
    def frontend_missing() -> dict[str, str]:
        return {
            "error": "Frontend not built",
            "hint": "Run npm run build in frontend/ or deploy via Docker",
            "dist_path": str(dist_path),
        }
