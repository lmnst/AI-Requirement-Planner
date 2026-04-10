from unittest import case

from fastapi.testclient import TestClient
# import sys
# import os
import app.main as main
from app.main import app
import app.services.llm_service as services

client = TestClient(app)




def test_generate_plan_empty_requirement_returns_400():
    response = client.post("/generate-plan", json={"requirement": ""})
    
    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "Requirement cannot be empty."

def test_generate_plan_happy_requirement_returns_200(monkeypatch):
    class FakeResponse:
        output_text = '{"summary":"ok","tasks":["a"],"implementation_plan":["b"],"test_checklist":["c"]}'

    def fake_create(*args, **kwargs):
        return FakeResponse()
    

    monkeypatch.setattr(services.client.responses, "create", fake_create)
    response = client.post("/generate-plan", json={"requirement": "做个todo"})

    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "ok"
    assert data["tasks"] == ["a"]
    assert data["implementation_plan"] == ["b"]
    assert data["test_checklist"] == ["c"]

def test_generate_plan_invalid_json_returns_500(monkeypatch):
    class FakeResponse:
        output_text = "..."

    def fake_create(*args, **kwargs):
        return FakeResponse()
    
    monkeypatch.setattr(services.client.responses, "create", fake_create)
    response = client.post("/generate-plan", json={"requirement": "做个todo"})

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Model did not return valid JSON."


def test_generate_test_cases_empty_requirement_returns_400():
   response =  client.post("/generate-test-cases", json={"requirement": ""})

   assert response.status_code == 400

   data = response.json()
   assert data["detail"] == "Requirement cannot be empty."

def test_generate_test_cases_happy_requirement_returns_200(monkeypatch):
    class fake_response:
        output_text = '{"feature_summary":"ok", "test_scenarios": ["a"], "edge_cases": ["b"]}'

    def fake_response_create(*args, **kwargs):
        return fake_response()
    
    monkeypatch.setattr(services.client.responses, "create", fake_response_create)

    response = client.post("/generate-test-cases", json={"requirement": "str"})

    assert response.status_code == 200
    data = response.json()
    assert data["feature_summary"] == "ok"
    assert data["test_scenarios"] == ["a"]
    assert data["edge_cases"] == ["b"]

def test_generate_test_cases_invalid_json_returns_500(monkeypatch):
    class fake_response:
        output_text = "..."

    def fake_response_create(*args, **kwargs):
        return fake_response()
    
    monkeypatch.setattr(services.client.responses, "create", fake_response_create)

    response = client.post("/generate-test-cases", json={"requirement": "str"})

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Model did not return valid JSON."

