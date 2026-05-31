def is_devops_role(title: str, description: str):
    text = (title + " " + description).lower()

    keywords = [
        "devops",
        "site reliability",
        "sre",
        "infrastructure",
        "platform engineer",
        "cloud",
        "kubernetes",
        "terraform",
        "ci/cd",
        "aws",
        "azure",
        "gcp",
        "docker"
    ]

    return any(kw in text for kw in keywords)
