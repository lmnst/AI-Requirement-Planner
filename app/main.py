from fastapi import FastAPI
from app.routes.planner import router as planner_router

app = FastAPI(title="AI Requirement Planner")

app.include_router(planner_router)

