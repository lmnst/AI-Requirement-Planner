from typing import Type, TypeVar

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, ValidationError
from openai import OpenAI
import json

Text_generate_plan = """
You are a software engineering planning assistant.

Return ONLY valid JSON with exactly these keys:
summary
tasks
implementation_plan
test_checklist
summary must be a string
each item in tasks must be a string
each item in implementation_plan must be a string
each item in test_checklist must be a string
do not return nested objects
do not return task/details, phase/steps, or category/items
"""

Text_Test_Cases = """
You are a software engineering planning assistant.

Return ONLY valid JSON with exactly these keys:
feature_summary
test_scenarios
edge_cases

feature_summary must be a string
each item in test_scenarios must be a string
each item in edge_cases must be a string
do not return objects inside arrays
do not return additional keys
"""

app = FastAPI()
client = OpenAI()

# def requirementModel
class RequirementRequest(BaseModel):
    requirement: str

# class ImplementationStep(BaseModel):
#     step: int
#     title: str

class responseModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    summary: str
    tasks: list[str]

# def PlanResponseMode
class PlanResponse(responseModel):
    # implementation_plan: list[ImplementationStep]
    implementation_plan: list[str]
    test_checklist: list[str]

# def TestCasesMode
class TestCases(BaseModel):
    #edge_cases: list[str]
    model_config = ConfigDict(extra='forbid')
    feature_summary: str
    test_scenarios: list[str]
    edge_cases: list[str]



def validate_requirement(request: RequirementRequest):
    if not request.requirement.strip():
        raise HTTPException(status_code=400, detail="Requirement cannot be empty.")

T = TypeVar('T', bound=BaseModel)

def call_openai_with_prompt(input_content: str, request: RequirementRequest):
    response = client.responses.create(
        model="gpt-5.4-nano",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": input_content
            },
            {
                "role": "user",
                "content": request.requirement
            }
        ],
    )
    return response

def parse_llm_json(response, output: Type[T]) -> T:
    try:
        result = json.loads(response.output_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model did not return valid JSON.")
    try:
        result = output(**result)
        return result
    except ValidationError as e:
        print(response.output_text)
        raise HTTPException(status_code=500, detail=f"Wrong DataFormat From AI: {e}")
    

# endpoint 1
@app.post("/generate-plan", response_model=PlanResponse)
async def generate_plan(request: RequirementRequest):

    # empty request validate 
    validate_requirement(request)

    # call LLM then return Response
    response = call_openai_with_prompt(Text_generate_plan, request)
    
    result = parse_llm_json(response, PlanResponse)
    return result

# endpoint2
@app.post("/generate-test-cases", response_model=TestCases)
def generate_test_cases(request: RequirementRequest):
    
    # empty request validate 
    validate_requirement(request)
    
    # call LLM then return Response
    response = call_openai_with_prompt(Text_Test_Cases, request)

    result = parse_llm_json(response, TestCases)
    return result

# def test_missing_field():
#     # 1. 模拟一个缺了 summary 的响应
#     mock_response = Response(output_text='{"tasks": ["学习Python"]}') 
    
#     # 2. 尝试运行你的函数，看它是否如期“爆炸”
#     # 注意：这里我们预期它会抛出 HTTPException
#     try:
#         parse_llm_json(mock_response, PlanResponse)
#         assert False, "函数没有报错，这不科学！"
#     except HTTPException as e:
#         assert e.status_code == 500  # 检查是不是你代码里写的那个 500
#         assert "Wrong DataFormat" in e.detail # 检查报错信息