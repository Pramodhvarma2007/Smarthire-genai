import json
from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError
from src.config import API_KEY, LLM_MODEL

client = genai.Client(api_key=API_KEY)


class Experience(BaseModel):
    role: str = ""
    company: str = ""
    duration: str = ""
    summary: str = ""


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""


class Profile(BaseModel):
    name: str = ""
    email: str = ""
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[Education] = []
    target_role: str = ""


PROMPT = """You are a resume reader. Extract details from the resume below.
Return ONLY valid JSON with exactly these keys:
name, email, skills (list of strings), experience (list of objects with
role, company, duration, summary), education (list of objects with
degree, institution, year), target_role (the job the person seems to want).
Rules:
- Use only information that is in the resume.
- If something is missing, use "" or an empty list.
- Do not add any text outside the JSON.

Resume:
{resume_text}
"""


def parse_resume(resume_text):
    last_error = None
    for attempt in range(2):  # try once, retry once
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=PROMPT.format(resume_text=resume_text),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0,
            ),
        )
        raw = response.text
        try:
            return Profile(**json.loads(raw))
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
    raise ValueError(f"Could not get valid JSON: {last_error}")