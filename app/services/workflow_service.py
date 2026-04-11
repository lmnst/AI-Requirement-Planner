from app.schemas import PlanResponse, RequirementRequest, WorkflowResponse
from app.services.planner_service import generate_plan, generate_test_cases


def build_test_case_request(request: str, plan: PlanResponse) -> RequirementRequest:
        new_requirement_string = f"""
Original requirement:
{request.requirement}

Generated plan:
{plan.model_dump_json(indent=2)}

Please generate test cases based on the original requirement and the generated plan above.
"""
        new_requirement = RequirementRequest(requirement = new_requirement_string)
        return new_requirement


async def generate_workflow(request: RequirementRequest):

    result_generate_plan = await generate_plan(request)
    
    request_new = build_test_case_request(request, result_generate_plan)

    result_generate_test_cases = await generate_test_cases(request_new)

    finally_result = WorkflowResponse(plan = result_generate_plan, test_cases = result_generate_test_cases)

    return finally_result