from app.config import ensure_openai_api_key

ensure_openai_api_key()

from fastapi import FastAPI  # noqa: E402
from mangum import Mangum  # noqa: E402

from app.routes.planner import router as planner_router  # noqa: E402

app = FastAPI(title="AI Requirement Planner")

app.include_router(planner_router)

handler = Mangum(app, lifespan="off")
