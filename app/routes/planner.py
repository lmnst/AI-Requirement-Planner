from fastapi import APIRouter

from app.schemas import PlanResponse, RequirementRequest, TestCases

import app.services.planner_service as planner_service

router = APIRouter()


@router.post("/generate-plan", response_model=PlanResponse)
async def generate_plan_route(request: RequirementRequest):
    result = await planner_service.generate_plan(request)
    return result


@router.post("/generate-test-cases", response_model=TestCases)
async def generate_test_cases_route(request: RequirementRequest):
    result = await planner_service.generate_test_cases(request)
    return result