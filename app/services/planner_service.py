from app.prompt import Text_Test_Cases, Text_generate_plan
from app.schemas import PlanResponse, RequirementRequest, TestCases
from app.services.llm_service import call_openai_with_prompt
from app.utils import parse_llm_json, validate_requirement


async def generate_plan(request: RequirementRequest):

    # empty request validate 
    validate_requirement(request)

    # call LLM then return Response
    response = call_openai_with_prompt(Text_generate_plan, request)
    
    result = parse_llm_json(response, PlanResponse)
    return result


async def generate_test_cases(request: RequirementRequest):
    
    # empty request validate 
    validate_requirement(request)
    
    # call LLM then return Response
    response = call_openai_with_prompt(Text_Test_Cases, request)

    result = parse_llm_json(response, TestCases)
    return result

