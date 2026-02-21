"""
Shared Gemini client using Google AI (generativelanguage.googleapis.com).
Uses an API key sourced from the environment — generated from GCP programmatically,
so no manual key management is needed.
"""
import os
import subprocess
import json
import requests

_cached_key: str | None = None

def _get_api_key() -> str:
    global _cached_key
    if _cached_key:
        return _cached_key

    # 1. Try env var first
    key = os.getenv("GEMINI_API_KEY")
    if key:
        _cached_key = key
        return key

    # 2. Fallback: fetch from gcloud (requires `gcloud alpha` installed)
    try:
        name_result = subprocess.run(
            ["gcloud", "alpha", "services", "api-keys", "list",
             "--project=gen-lang-client-0147867042",
             "--format=value(name)"],
            capture_output=True, text=True, timeout=15
        )
        resource_name = name_result.stdout.strip().splitlines()[0]
        key_result = subprocess.run(
            ["gcloud", "alpha", "services", "api-keys", "get-key-string",
             resource_name, "--format=value(keyString)"],
            capture_output=True, text=True, timeout=15
        )
        key = key_result.stdout.strip()
        if key:
            _cached_key = key
            return key
    except Exception as e:
        pass

    raise ValueError(
        "No GEMINI_API_KEY found. Set it in .env or ensure gcloud alpha is configured.\n"
        "Quick fix: add GEMINI_API_KEY=<your_key> to .env"
    )


def generate(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    """Call Gemini REST API. No OAuth scopes needed — just an API key."""
    key = _get_api_key()
    # Strip 'models/' prefix if caller included it
    model_id = model_name.replace("models/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={key}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=body, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"Gemini Error {response.status_code}: {response.text[:300]}")

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def get_model(model_name: str = "gemini-2.5-flash"):
    """Compatibility shim returning an object with .generate_content()."""
    class _Model:
        def __init__(self, name): self.name = name
        def generate_content(self, prompt):
            if isinstance(prompt, list):
                prompt = " ".join(p for p in prompt if isinstance(p, str))
            class _Resp:
                def __init__(self, t): self.text = t
            return _Resp(generate(prompt, self.name))
    return _Model(model_name)
