from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
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

class RequirementRequest(BaseModel):
    requirement: str

# class ImplementationStep(BaseModel):
#     step: int
#     title: str

class responseModel(BaseModel):
    summary: str
    tasks: list[str]

class PlanResponse(responseModel):
    # implementation_plan: list[ImplementationStep]
    implementation_plan: list[str]
    test_checklist: list[str]

class TestCases(BaseModel):
    #edge_cases: list[str]
    feature_summary: str
    test_scenarios: list[str]
    edge_cases: list[str]



@app.post("/generate-plan", response_model=PlanResponse)
async def generate_plan(request: RequirementRequest):
    #The if not statement in Python is used to execute a block of code when a condition evaluates to False.
    if not request.requirement.strip():
        raise HTTPException(status_code=400, detail="Requirement cannot be empty.")
    
    response = client.responses.create(
        model="gpt-5.4-nano",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": Text_generate_plan
            },
            {
                "role": "user",
                "content": request.requirement
            }
        ],
        #text_format=PlanResponse #这样写是对的吗？？
        #不对，这个有错
    )

    try:
        result = json.loads(response.output_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model did not return valid JSON.")

    try:
        result = PlanResponse(**result)
        return result
    except ValidationError as e:
        print(response.output_text)
        raise HTTPException(status_code=500, detail=f"Wrong DataFormat From AI: {e}")
   

@app.post("/generate-test-cases", response_model=TestCases)
def generate_test_cases(request: RequirementRequest):
    if not request.requirement.strip():
        raise HTTPException(status_code=400, detail="Requirement cannot be empty.")
    
    response = client.responses.create(
        model="gpt-5.4-nano",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": Text_Test_Cases
            },
            {
                "role": "user",
                "content": request.requirement
            }
        ],
        #text_format=TestCases 不对，这个有错
    )

    try:
        result = json.loads(response.output_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model did not return valid JSON.")

    try:
        result = TestCases(**result)
        return result
    except ValidationError as e:
        print(response.output_text)
        raise HTTPException(status_code=422, detail=f"Wrong DataFormat From AI: {e}")


# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello! That's my FIRST FastAPI interface"}

# @app.get("/hello/{name}")
# def say_hello(name: str):
#     return {"message": f"Hello, {name}! Welcome to the Backend world!"}

