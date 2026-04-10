# AI Requirement Planner

A minimal but structured AI backend project built with **Python, FastAPI, OpenAI API, Pydantic, and Pytest**.

This project takes a natural-language software requirement as input and converts it into structured JSON outputs for:

* implementation planning
* test case generation

The focus of this project is not just calling an LLM, but building a **reliable backend pipeline** around it:

* structured output parsing
* schema validation with Pydantic
* defensive error handling
* test coverage for both success and failure cases
* clean project layering with routes / services / schemas / utils

---

## Features

### 1. Generate implementation plans

`POST /generate-plan`

Input a requirement description and return a structured development plan:

* summary
* tasks
* implementation plan
* test checklist

### 2. Generate test cases

`POST /generate-test-cases`

Input a requirement description and return structured test suggestions:

* feature summary
* test scenarios
* edge cases

### 3. Structured output enforcement

LLM responses are parsed with `json.loads()` and validated using Pydantic models.

### 4. Defensive error handling

The backend handles common failure modes such as:

* empty input
* invalid JSON returned by the model
* missing required fields
* unexpected extra fields

### 5. Automated tests

Pytest is used to verify:

* happy path behavior
* empty input handling
* invalid JSON handling
* schema validation failures

---

## Tech Stack

* **Python**
* **FastAPI**
* **OpenAI API**
* **Pydantic**
* **Pytest**

---

## Project Structure

```text
AI-Requirement-Planner/
├─ app
│  ├─ config.py
│  ├─ main.py
│  ├─ prompt.py
│  ├─ routes
│  │  ├─ planner.py
│  │  └─ __init__.py
│  ├─ schemas.py
│  ├─ services
│  │  ├─ llm_service.py
│  │  ├─ planner_service.py
│  │  └─ __init__.py
│  ├─ utils.py
│  └─ __init__.py
├─ README.md
├─ requirements.txt
└─ tests
   ├─ test_main.py
   ├─ test_parser.py
   └─ Test.py
```

---

## Architecture Overview

### `app/main.py`

FastAPI application entrypoint.

### `app/routes/planner.py`

Defines the API endpoints:

* `/generate-plan`
* `/generate-test-cases`

This layer is responsible only for request/response handling.

### `app/services/llm_service.py`

Encapsulates OpenAI API calls.

### `app/services/planner_service.py`

Contains the core business logic:

* validate request input
* prepare prompts
* call the LLM service
* parse and validate model output

### `app/schemas.py`

Defines Pydantic request/response models.

### `app/utils.py`

Contains shared utility logic such as JSON parsing and validation helpers.

### `app/config.py`

Stores configuration such as model settings and environment variables.

---

## API Endpoints

### `POST /generate-plan`

#### Request

```json
{
  "requirement": "Build a todo app with add, delete, and filter features."
}
```

#### Response

```json
{
  "summary": "A todo application with task management and filtering capabilities.",
  "tasks": [
    "Design API endpoints",
    "Implement CRUD logic",
    "Add filtering support"
  ],
  "implementation_plan": [
    "Create task schema",
    "Build FastAPI routes",
    "Implement service logic"
  ],
  "test_checklist": [
    "Test task creation",
    "Test task deletion",
    "Test filtering behavior"
  ]
}
```

---

### `POST /generate-test-cases`

#### Request

```json
{
  "requirement": "Build a todo app with add, delete, and filter features."
}
```

#### Response

```json
{
  "feature_summary": "Todo app with task creation, deletion, and filtering.",
  "test_scenarios": [
    "Add a new task successfully",
    "Delete an existing task",
    "Filter tasks by status"
  ],
  "edge_cases": [
    "Submitting an empty task",
    "Deleting a non-existent task",
    "Applying an unsupported filter"
  ]
}
```

---

## Error Handling

This project explicitly validates both user input and LLM output.

Examples of handled errors:

* empty `requirement`
* invalid JSON returned by the LLM
* missing required fields in parsed output
* extra unexpected fields when schema forbids them

This helps make the API response more stable and predictable for downstream consumers.

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/lmnst/AI-Requirement-Planner.git
cd AI-Requirement-Planner
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

If your project uses additional config fields, add them here as well.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

### 6. Open API docs

FastAPI automatically provides interactive documentation at:

* `http://127.0.0.1:8000/docs`

---

## Running Tests

Run all tests:

```bash
pytest
```

Or run specific test files:

```bash
pytest tests/test_main.py
pytest tests/test_parser.py
```

---

## What This Project Demonstrates

This project demonstrates practical backend engineering around LLM output:

* turning free-form requirements into structured data
* validating model responses before returning them
* separating API layer from business logic
* writing tests for both normal and failure cases
* building an AI backend that is more robust than a simple prompt wrapper

---

## Limitations

Current limitations include:

* single-step generation only
* no workflow orchestration yet
* no persistence layer
* no retry / logging / observability pipeline yet
* output quality still depends on prompt quality and model behavior

---

## Next Steps

Planned improvements:

* add a multi-step workflow endpoint
* chain plan generation and test generation
* introduce logging and better observability
* improve prompt management
* move toward agent/workflow-style orchestration

---

## Learning Goal

This project was built as a hands-on step from:

* basic API development
* to structured AI backend engineering
* and eventually toward workflow / agent-based systems

It is intentionally small in scope, but designed to be extended incrementally.

API-Study
├─ app
│  ├─ config.py
│  ├─ main.py
│  ├─ prompt.py
│  ├─ routes
│  │  ├─ planner.py
│  │  └─ __init__.py
│  ├─ schemas.py
│  ├─ services
│  │  ├─ llm_service.py
│  │  ├─ planner_service.py
│  │  └─ __init__.py
│  ├─ utils.py
│  └─ __init__.py
├─ README.md
├─ requirements.txt
└─ tests
   ├─ Test.py
   ├─ test_main.py
   └─ test_parser.py

```