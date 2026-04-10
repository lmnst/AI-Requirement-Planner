import json
from typing import Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel, ValidationError

from app.schemas import RequirementRequest


T = TypeVar('T', bound=BaseModel)


def validate_requirement(request: RequirementRequest):
    if not request.requirement.strip():
        raise HTTPException(status_code=400, detail="Requirement cannot be empty.")

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
 