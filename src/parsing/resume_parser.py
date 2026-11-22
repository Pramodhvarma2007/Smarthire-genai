import json
from typing import List
from pydantic import BaseModel, ValidationError
from src.llm import call_llm
from src.generate.prompts import PARSER_PROMPT_V2


class Experience(BaseModel):
    role: str = ""
    company: str = ""
    duration: str = ""
    summary: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    tech: List[str] = []


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""


class Profile(BaseModel):
    name: str = ""
    email: str = ""
    skills: List[str] = []
    soft_skills: List[str] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    education: List[Education] = []
    target_role: str = ""


def parse_resume(resume_text, prompt=PARSER_PROMPT_V2):
    last_error = None
    for _ in range(2):
        raw = call_llm(prompt.format(resume_text=resume_text),
                       json_mode=True, temperature=0)
        try:
            return Profile(**json.loads(raw))
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
    raise ValueError(f"Could not get valid JSON: {last_error}")