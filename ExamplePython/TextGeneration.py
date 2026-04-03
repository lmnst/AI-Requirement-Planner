import sys
from openai import OpenAI
from pydantic import BaseModel
client = OpenAI()

# response = client.responses.create(
# model="gpt-4o-2024-08-06",
# input=[
# {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
# {"role": "user", "content": "how can I solve 8x + 7 = -23"}
# ],
# text={
# "format": {
# "type": "json_schema",
# "name": "math_response",
# "schema": {
# "type": "object",
# "properties": {
# "steps": {
# "type": "array",
# "items": {
# "type": "object",
# "properties": {
# "explanation": {"type": "string"},
# "output": {"type": "string"}
# },
# "required": ["explanation", "output"],
# "additionalProperties": False
# }
# },
# "final_answer": {"type": "string"}
# },
# "required": ["steps", "final_answer"],
# "additionalProperties": False
# },
# "strict": True
# }
# }
# )

# print(response.output_text)

# print(response.output_text)

# class Step(BaseModel):
#     explanation: str
#     output: str

# class MathReasoning(BaseModel):
#     steps: list[Step]
#     final_answer: str

# response = client.responses.parse(
#     model="gpt-4o-mini",
#     input=[
#         {
#             "role": "system",
#             "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
#         },
#         {"role": "user", "content": "how can I solve 8x + 7 = -23"},
#     ],
#     text_format=MathReasoning,
# )

# math_reasoning = response.output_parsed

# print(math_reasoning)


# class CalendarEvent(BaseModel):
#     name: str
#     date: str
#     participants: list[str]

# response = client.responses.parse(
#     model="gpt-4o-mini",
#     input=[
#         {"role": "system", "content": "Extract the event information."},
#         {
#             "role": "user",
#             "content": "Alice and Bob are going to a science fair on Friday.",
#         },
#     ],
#     text_format=CalendarEvent,
# )

# event = response.output_parsed

# print(event)

# response = client.responses.create(
#     model = "gpt-5.4-nano",
#     reasoning={"effort": "low"},
#     instructions="Talk like a pirate.",
#     input="Are semicolons optional in JS?",
# )

# user_input = " ".join(sys.argv[1:])

# if not user_input:
#     print("Please provide something")
#     sys.exit(1)

# text="""
# I am learning the OpenAI API.
# I only want a quick overview, not deep theory.
# I want to understand what to do after the quickstart.
# """

# dev_content = """
# You are a software engineering assistant.
# Given a requirement, produce output in the following format:

# Summary:
# - ...

# Task Breakdown:
# 1. ...
# 2. ...
# 3. ...

# Implementation Plan:
# - ...

# Test Checklist:
# - ...

# Keep the answer concise and practical.
# """

# response = client.responses.create(
#     model="gpt-5.4-nano",
#     reasoning={"effort": "low"},
#     input=[
#         {
#             "role": "developer",
#             "content": dev_content
#         },
#         {
#             "role": "user",
#             "content": user_input
#         }
#     ]
# )



# print(response.output_text)
