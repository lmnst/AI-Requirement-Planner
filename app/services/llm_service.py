from openai import OpenAI

from app.schemas import RequirementRequest


client = OpenAI()

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