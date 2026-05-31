import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_TEXT = 4000   # limit tokens


def shorten(text, limit=MAX_TEXT):
    """Trim long text to avoid token errors"""
    if not text:
        return ""
    return text[:limit]


def generate_tailored_resume(resume_text, job_description):

    resume_text = shorten(resume_text)
    job_description = shorten(job_description)

    prompt = f"""
Rewrite the resume to better match this job.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content