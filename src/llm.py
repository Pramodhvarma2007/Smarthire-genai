import time
from google import genai
from google.genai import types
from src.config import API_KEY, LLM_MODEL, FALLBACK_MODEL

client = genai.Client(api_key=API_KEY)


def call_llm(prompt, json_mode=False, temperature=0.3):
    config = types.GenerateContentConfig(
        temperature=temperature,
        response_mime_type="application/json" if json_mode else "text/plain",
    )
    for model in (LLM_MODEL, FALLBACK_MODEL):
        for attempt in range(3):
            try:
                r = client.models.generate_content(
                    model=model, contents=prompt, config=config)
                return r.text
            except Exception as e:
                print(f"[retry] {model} attempt {attempt + 1}: {e}")
                time.sleep(2 * (attempt + 1))
    raise RuntimeError("LLM unavailable after retries")