from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from app.config import settings

T = TypeVar("T", bound=BaseModel)

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def structured_completion(
    system_prompt: str,
    user_prompt: str,
    output_model: type[T],
) -> T:
    client = get_client()
    response = client.chat.completions.parse(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=output_model,
    )
    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Empty LLM response")
    return parsed
