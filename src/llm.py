import hashlib
import json
import os
import time
from google import genai
from google.genai import types
from src.config import API_KEY, MODEL_CHAIN

client = genai.Client(api_key=API_KEY)
CACHE_PATH = "vectorstore/llm_cache.json"
_cache = None


def _get_cache():
    global _cache
    if _cache is None:
        try:
            with open(CACHE_PATH, encoding="utf-8") as f:
                _cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _cache = {}
    return _cache


def _save_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(_cache, f)


def call_llm(prompt, json_mode=False, temperature=0.3, use_cache=True):
    key = hashlib.sha256(f"{json_mode}|{temperature}|{prompt}".encode()).hexdigest()
    cache = _get_cache()
    if use_cache and key in cache:
        return cache[key]

    config = types.GenerateContentConfig(
        temperature=temperature,
        response_mime_type="application/json" if json_mode else "text/plain",
    )
    for model in MODEL_CHAIN:
        for attempt in range(3):
            try:
                r = client.models.generate_content(
                    model=model, contents=prompt, config=config)
                cache[key] = r.text
                _save_cache()
                return r.text
            except Exception as e:
                msg = str(e)
                if any(w in msg for w in ("429", "RESOURCE_EXHAUSTED", "404", "NOT_FOUND")):
                    print(f"[limit] {model} limit reached, trying next model")
                    break  # no point retrying a used-up limit
                print(f"[retry] {model} attempt {attempt + 1}: {msg[:120]}")
                time.sleep(2 * (attempt + 1))
    raise RuntimeError("The AI model is busy or its daily limit is used up. Try again later.")