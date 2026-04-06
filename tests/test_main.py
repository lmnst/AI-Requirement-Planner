from fastapi.testclient import TestClient
import sys
import os
import main
from main import app

Client = TestClient(app)

def test_generate_plan_empty_requirement_returns_400():
    response = Client.post("/generate-plan", json={"requirement": ""})
    
    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "Requirement cannot be empty."

def test_generate_plan_happy_requirement_returns_200(monkeypatch):
    class FakeResponse:
        output_text = '{"summary":"ok","tasks":["a"],"implementation_plan":["b"],"test_checklist":["c"]}'

    def fake_create(*args, **kwargs):
        return FakeResponse()
    

    monkeypatch.setattr(main.client.responses, "create", fake_create)
    response = Client.post("/generate-plan", json={"requirement": "做个todo"})

    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "ok"
    assert data["tasks"] == ["a"]
    assert data["implementation_plan"] == ["b"]
    assert data["test_checklist"] == ["c"]

def test_generate_plan_invalid_json_returns_500(monkeypatch):
    class FakeResponse:
        output_text = ""

    def fake_create(*args, **kwargs):
        return FakeResponse()
    
    monkeypatch.setattr(main.client.responses, "create", fake_create)
    response = Client.post("/generate-plan", json={"requirement": "做个todo"})

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Model did not return valid JSON."




    
    
    
    
    # detail == "Requirement cannot be empty."
    # assert response.json() == {
    #     "summary": str,
    #     "tasks": list[str],
    #     "implementation_plan": list[str],
    #     "test_checklist": list[str],
    # }


# summary
# tasks
# implementation_plan
# test_checklist
# class TestResponses(unittest.TestCase):

#     #状态码是 200
#     def test_01(self):
#         value =  {"summary": "str", "tasks": "str", "implementation_plan": "str", "test_checklist": "str"}
#         #mort
#         output_test = mock.patch.object(app.generate_plan(), "response.output_text", value)
#         assert json.loads(output_test).status_code() == 200
