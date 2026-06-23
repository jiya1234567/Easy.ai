"""
mistral_client.py
==================
Thin wrapper around a local Mistral model (via Ollama) that returns
structured JSON. Used by every reasoning stage in the Theory Engine
pipeline (Hypothesis Agent, Counterfactual Engine, Theory Engine,
Discovery Planner).

Prerequisites:
    1. Install Ollama: https://ollama.com
    2. Pull a Mistral model:
           ollama pull mistral
       (or "mistral:7b-instruct" for the instruction-tuned variant)
    3. pip install ollama
"""

import json
import re
from typing import Any, Optional

import ollama


DEFAULT_MODEL = "mistral"


class MistralClient:
    """Wrapper that enforces structured JSON output from a local Mistral model."""

    def __init__(self, model: str = DEFAULT_MODEL, host: Optional[str] = None):
        self.model = model
        self._client = ollama.Client(host=host) if host else ollama.Client()

    def _strip_code_fences(self, text: str) -> str:
        """Remove ```json ... ``` or ``` ... ``` wrappers if present."""
        text = text.strip()
        fence_match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
        if fence_match:
            return fence_match.group(1).strip()
        return text

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.4,
        max_retries: int = 2,
    ) -> dict[str, Any]:
        """
        Call Mistral and parse the response as JSON.

        Raises ValueError if the model never returns valid JSON
        after max_retries attempts.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        last_error = None
        for attempt in range(max_retries + 1):
            response = self._client.chat(
                model=self.model,
                messages=messages,
                options={"temperature": temperature},
            )
            raw = response["message"]["content"]
            cleaned = self._strip_code_fences(raw)

            try:
                return json.loads(cleaned)
            except json.JSONDecodeError as e:
                last_error = e
                # Ask the model to fix its own output
                messages.append({"role": "assistant", "content": raw})
                messages.append({
                    "role": "user",
                    "content": (
                        "That was not valid JSON. Respond with ONLY a valid "
                        "JSON object, no prose, no markdown fences."
                    ),
                })

        raise ValueError(
            f"Mistral did not return valid JSON after {max_retries + 1} "
            f"attempts. Last error: {last_error}"
        )

    def generate_text(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
        """Plain-text generation, no JSON parsing."""
        response = self._client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": temperature},
        )
        return response["message"]["content"]


# ── Quick self-test ──────────────────────────────────────────────
if __name__ == "__main__":
    client = MistralClient()

    result = client.generate_json(
        system_prompt=(
            "You are a hypothesis-generation assistant. Respond ONLY with "
            "valid JSON, no other text."
        ),
        user_prompt=(
            'Given this observation: {"signal": "temperature", "trend": "rising", '
            '"correlated_with": "humidity"}, '
            'return a JSON object with keys "hypothesis" (string), '
            '"confidence" (float 0-1), and "variables" (list of strings).'
        ),
    )
    print(json.dumps(result, indent=2))
