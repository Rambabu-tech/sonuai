from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def compute_similarity(resume, job_desc):

    prompt = f"""
Score the match between resume and job from 0 to 1.

Resume:
{resume[:1500]}

Job:
{job_desc[:1500]}

Return ONLY a number like 0.75
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        score_text = response.choices[0].message.content.strip()
        score = float(score_text)

        return max(0, min(score, 1))

    except Exception as e:
        print("❌ AI Error:", e)
        return 0.3


# 🔥 THIS WAS MISSING (CRITICAL)
def decide_application(score):

    if score > 0.75:
        return "APPLY"
    elif score > 0.55:
        return "REVIEW"
    else:
        return "SKIP"