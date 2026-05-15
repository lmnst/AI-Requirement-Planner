import json
import os

import boto3

_LOADED = False


def ensure_openai_api_key() -> None:
    """Inject OPENAI_API_KEY into os.environ before any code constructs the OpenAI client.

    Resolution order:
      1. If OPENAI_API_KEY is already set, return.
      2. If OPENAI_SECRET_NAME is set, fetch the value from AWS Secrets Manager
         (using AWS_REGION env, default eu-central-1) and inject it.
      3. Otherwise raise RuntimeError so Lambda cold-start fails fast with a clear message.
    """
    global _LOADED
    if _LOADED:
        return

    if os.environ.get("OPENAI_API_KEY"):
        _LOADED = True
        return

    secret_name = os.environ.get("OPENAI_SECRET_NAME")
    if not secret_name:
        raise RuntimeError(
            "OPENAI_API_KEY is not set and OPENAI_SECRET_NAME is not configured; "
            "set OPENAI_API_KEY locally or configure OPENAI_SECRET_NAME for Lambda."
        )

    region = os.environ.get("AWS_REGION", "eu-central-1")
    client = boto3.client("secretsmanager", region_name=region)
    resp = client.get_secret_value(SecretId=secret_name)
    raw = resp.get("SecretString") or ""

    try:
        parsed = json.loads(raw)
        value = parsed.get("OPENAI_API_KEY", raw) if isinstance(parsed, dict) else raw
    except json.JSONDecodeError:
        value = raw

    if not value:
        raise RuntimeError(
            f"Secrets Manager secret '{secret_name}' returned an empty value for OPENAI_API_KEY."
        )

    os.environ["OPENAI_API_KEY"] = value
    _LOADED = True
