# AI Requirement Planner

A minimal AI backend project built with **Python**, **FastAPI**, and the **OpenAI API**.

This project takes a natural-language software requirement and turns it into structured JSON for two practical backend use cases:

- **development planning**
- **test case generation**

The focus of this project is not building a large product.  
The focus is building a clean, testable AI backend workflow:

**validate request -> call LLM -> parse JSON -> enforce schema -> return stable API response**

---

## Overview

LLMs are useful, but raw model output is unreliable if you want to build backend services on top of it.

This project addresses that by wrapping the model behind a FastAPI service and adding a validation layer before anything is returned to the client.

The backend currently provides:

- a planning endpoint for structured implementation output
- a test-case endpoint for structured QA-oriented output
- schema validation with Pydantic
- defensive error handling for malformed model responses
- automated tests for both endpoint behavior and parser behavior

This makes the project a compact example of how to build a **structured-output AI backend** instead of a free-form chatbot API. :contentReference[oaicite:1]{index=1}

---

## Features

### 1. Generate implementation plans
`POST /generate-plan`

Given a software requirement, the API returns a structured plan with these fields:

- `summary`
- `tasks`
- `implementation_plan`
- `test_checklist`

### 2. Generate test cases
`POST /generate-test-cases`

Given the same kind of requirement input, the API returns structured testing output with these fields:

- `feature_summary`
- `test_scenarios`
- `edge_cases`

### 3. Enforce predictable output
The backend does not trust model output blindly.

It explicitly:

- parses the LLM response as JSON
- validates it against a target schema
- rejects malformed JSON
- rejects missing required fields
- rejects extra fields through `extra='forbid'`

That design choice is the core engineering idea of the project. :contentReference[oaicite:2]{index=2}

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- OpenAI Python SDK
- Pytest

---

## Project Structure

```bash
AI-Requirement-Planner/
├── main.py
├── tests/
│   ├── test_main.py
│   └── test_parser.py
├── .env.example
├── requirements.txt
└── README.md