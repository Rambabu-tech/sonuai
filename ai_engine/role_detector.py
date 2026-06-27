from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_role(resume_text):

    prompt = f"""
Extract the TOP 3 job roles from this resume.

Only return roles as a list.

Resume:
{resume_text[:1500]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        roles = response.choices[0].message.content.strip()

        return roles

    except Exception as e:
        print("❌ Role detection error:", e)
        return "software engineer"

