from openai import OpenAI

client = OpenAI()

def generate_answer(question, resume_text):

    try:
        prompt = f"""
You are a job applicant.

Resume:
{resume_text}

Question:
{question}

Answer professionally in 2-4 lines.
"""

        response = client.chat.completions.create(
            model="gpt-5-5-instant",   # ✅ FIXED MODEL
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ AI error:", e)
        return "I am very interested in this opportunity."