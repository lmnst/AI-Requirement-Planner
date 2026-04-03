import sys
import json
from openai import OpenAI

client = OpenAI()

user_input = " ".join(sys.argv[1:])

if not user_input:
    print("Please provide a requirement.")
    sys.exit(1)

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

Rules:
- summary: string
- tasks: array of strings
- implementation_plan: array of strings
- test_checklist: array of strings
- Do not include markdown
- Do not include explanation outside JSON
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)


try:
    result = json.loads(response.output_text)
    required_keys = ["summary", "tasks", "implementation_plan", "test_checklist"]
    for key in required_keys:
        if key not in result:
            print(f"Missing key: {key}")

    print(json.dumps(result, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("Model did not return valid JSON.")
    print(response.output_text)

# print(response.output_text)