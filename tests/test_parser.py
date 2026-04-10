import json
import pytest
from fastapi import HTTPException
from app.schemas import PlanResponse, TestCases
from app.utils import parse_llm_json


VALID_PLAN_RESPONSE = {
    "summary": "ok",
    "tasks": ["a"],
    "implementation_plan": ["b"],
    "test_checklist": ["c"],
}

VALID_TEST_CASES = {
    "feature_summary": "ok",
    "test_scenarios": ["a"],
    "edge_cases": ["b"],
}


def make_missing_field_cases(payload):
    cases = []
    for key in payload:
        temp_dict = payload.copy()
        temp_dict.pop(key)
        cases.append(temp_dict)
    return cases


class FakeResponse:
    def __init__(self, output_text: str):
        self.output_text = output_text


@pytest.mark.parametrize(
    "valid_payload,response_model,expected_json",
    [
        (VALID_PLAN_RESPONSE, PlanResponse, VALID_PLAN_RESPONSE),
        (VALID_TEST_CASES, TestCases, VALID_TEST_CASES),
    ],
)
def test_parse_valid_json(valid_payload, response_model, expected_json):
    response = FakeResponse(json.dumps(valid_payload))
    result = parse_llm_json(response, response_model)

    assert result.model_dump() == expected_json


def test_parse_llm_json_invalid_json():
    response = FakeResponse("this is not json")

    with pytest.raises(HTTPException) as exc_info:
        parse_llm_json(response, PlanResponse)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Model did not return valid JSON."


@pytest.mark.parametrize(
    "bad_payload,response_model",
    [(payload, PlanResponse) for payload in make_missing_field_cases(VALID_PLAN_RESPONSE)]
    + [(payload, TestCases) for payload in make_missing_field_cases(VALID_TEST_CASES)],
)
def test_parse_llm_json_missing_required_field(bad_payload, response_model):
    response = FakeResponse(json.dumps(bad_payload))

    with pytest.raises(HTTPException) as exc_info:
        parse_llm_json(response, response_model)

    assert exc_info.value.status_code == 500
    assert "Wrong DataFormat From AI" in exc_info.value.detail