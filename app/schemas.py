# def requirementModel
from pydantic import BaseModel, ConfigDict


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
    
