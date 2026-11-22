from src.llm import call_llm
from src.generate.prompts import CV_SUGGEST_V1, CV_SUGGEST_V2


def suggest_improvements(profile, job_text, prompt=CV_SUGGEST_V1):
    return call_llm(
        prompt.format(resume_json=profile.model_dump_json(indent=2),
                      job_text=job_text),
        temperature=0.4)