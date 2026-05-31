import os
from openai import OpenAI

# Initialize OpenAI client safely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def match_job(title, description):
    """
    Returns:
        score (int)
        decision (str)
        reason (str)
    """

    prompt = f"""
You are an expert DevOps career assistant.

Candidate background:
- DevOps Engineer
- AWS, Azure
- Kubernetes
- Terraform
- CI/CD
- SRE
- Infrastructure Automation

Job Title:
{title}

Job Description:
{description}

Score this job 0-100 for DevOps relevance.

Return STRICT JSON:
{{
  "score": number,
  "decision": "APPLY" or "SKIP",
  "reason": "short explanation"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strict JSON generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        import json
        result = json.loads(content)

        score = int(result.get("score", 0))
        decision = result.get("decision", "SKIP")
        reason = result.get("reason", "")

        return score, decision, reason

    except Exception as e:
        print("AI match error:", e)
        return 0, "SKIP", "AI error"
