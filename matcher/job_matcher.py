def calculate_match_score(job_title, job_description, resume_text):

    title = job_title.lower()
    description = job_description.lower()
    resume = resume_text.lower()

    score = 0

    # -------------------------
    # Title match
    # -------------------------

    title_keywords = [
        "devops",
        "site reliability",
        "sre",
        "platform engineer",
        "cloud engineer",
        "infrastructure engineer"
    ]

    for word in title_keywords:
        if word in title:
            score += 0.4
            break

    # -------------------------
    # Skill overlap
    # -------------------------

    skills = [
        "aws",
        "terraform",
        "kubernetes",
        "docker",
        "ci/cd",
        "jenkins",
        "python",
        "linux",
        "ansible",
        "grafana",
        "prometheus"
    ]

    overlap = 0

    for skill in skills:
        if skill in description and skill in resume:
            overlap += 1

    score += overlap * 0.05

    return min(score, 1.0)
