from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def compute_similarity(resume, job_desc):

    prompt = f"""
You are an AI job matcher.

Compare this RESUME and JOB DESCRIPTION.

Give a match score from 0 to 1.

Resume:
{resume}

Job:
{job_desc}

Only return number like 0.85
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        score = float(response.choices[0].message.content.strip())
    except:
        score = 0.5

    return score


def decide_application(score):
    return "APPLY" if score > 0.6 else "SKIP"