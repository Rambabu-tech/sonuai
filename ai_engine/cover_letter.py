import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_cover_letter(resume, title, description):

    prompt = f"""
Write a short professional cover letter.

Job Title: {title}

Job Description:
{description[:2000]}

Candidate Resume:
{resume[:2000]}

Keep it under 200 words.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()