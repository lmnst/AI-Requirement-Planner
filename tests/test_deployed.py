import os

import pytest
import requests


API_BASE_URL = os.environ.get("API_BASE_URL")
REQUEST_TIMEOUT_SECONDS = 30


@pytest.fixture(scope="module")
def base_url() -> str:
    if not API_BASE_URL:
        pytest.skip("API_BASE_URL is not set; skipping deployed smoke tests")
    return API_BASE_URL.rstrip("/")


def test_generate_plan_smoke(base_url: str) -> None:
    payload = {"requirement": "build a simple todo app with add, delete, and filter"}
    url = f"{base_url}/generate-plan"

    try:
        resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} raised: {e!r}")

    if resp.status_code != 200:
        pytest.fail(
            f"Expected 200 from {url}, got {resp.status_code}. "
            f"Headers={dict(resp.headers)} Body={resp.text[:500]!r}"
        )

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response was not valid JSON. Body={resp.text[:500]!r}")

    for key in ("summary", "tasks", "implementation_plan", "test_checklist"):
        assert key in data, f"Missing key {key!r} in response. Keys present: {list(data.keys())}"

    assert isinstance(data["summary"], str) and data["summary"], "summary should be a non-empty string"
    assert isinstance(data["tasks"], list), "tasks should be a list"
    assert isinstance(data["implementation_plan"], list), "implementation_plan should be a list"
    assert isinstance(data["test_checklist"], list), "test_checklist should be a list"


def test_generate_plan_rejects_empty_requirement(base_url: str) -> None:
    url = f"{base_url}/generate-plan"
    try:
        resp = requests.post(url, json={"requirement": ""}, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} raised: {e!r}")

    assert resp.status_code == 400, (
        f"Expected 400 for empty requirement, got {resp.status_code}. Body={resp.text[:500]!r}"
    )
    body = resp.json()
    assert body.get("detail") == "Requirement cannot be empty.", body
