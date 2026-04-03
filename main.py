from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI()
client = OpenAI()

class RequirementRequest(BaseModel):
    requirement: str

@app.post("/generate-plan")
def generate_plan(request: RequirementRequest):
    if not request.requirement.strip():
        raise HTTPException(status_code=400, detail="Requirement cannot be empty.")
    
    response = client.responses.create(
        model="gpt-5.4-nano",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": """
You are a software engineering planning assistant.

Return ONLY valid JSON with exactly these keys:
summary
tasks
implementation_plan
test_checklist
"""
            },
            {
                "role": "user",
                "content": request.requirement
            }
        ]
    )

    try:
        result = json.loads(response.output_text)
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model did not return valid JSON.")
    


# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello! That's my FIRST FastAPI interface"}

# @app.get("/hello/{name}")
# def say_hello(name: str):
#     return {"message": f"Hello, {name}! Welcome to the Backend world!"}

