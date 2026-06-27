from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_skills(resume_text):

    prompt = f"""
Extract top technical skills from this resume.

Return ONLY comma separated skills.

Resume:
{resume_text[:2000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        skills = response.choices[0].message.content.strip().lower()
        return [s.strip() for s in skills.split(",")]

    except Exception as e:
        print("❌ Skill extraction error:", e)
        return []
