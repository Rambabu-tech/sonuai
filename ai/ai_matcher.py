import os


DEVOPS_KEYWORDS = [
    "devops", "sre", "infrastructure", "terraform", "aws", "azure",
    "gcp", "kubernetes", "docker", "ci/cd", "jenkins", "helm"
]


def ai_match(resume_text: str, job_description: str):
    """
    Lightweight Jobright-style scoring
    No OpenAI required
    """

    text = job_description.lower()
    matches = sum(1 for k in DEVOPS_KEYWORDS if k in text)

    score = min(60 + matches * 3, 96)

    decision = "APPLY" if score >= 85 else "SKIP"

    return {
        "score": score,
        "decision": decision,
        "reason": f"Matched {matches} DevOps/Infra signals"
    }
