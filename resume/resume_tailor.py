# resume/resume_tailor.py

import os
from docx import Document


def tailor_resume(title: str, description: str):
    """
    Simple tailoring logic.
    You can upgrade this later with AI.
    """

    base_resume_path = "data/resume.txt"

    if not os.path.exists(base_resume_path):
        return f"Tailored Resume for {title}\n\n{description}"

    with open(base_resume_path, "r") as f:
        base_content = f.read()

    tailored = f"""
{base_content}

--------------------------------
TARGET ROLE
--------------------------------
{title}

--------------------------------
ROLE KEYWORDS
--------------------------------
{description[:1000]}
"""

    return tailored


def save_resume(content: str, filename: str):
    """
    Saves DOCX resume
    """

    os.makedirs("data/generated_resumes", exist_ok=True)

    filepath = os.path.join("data/generated_resumes", filename)

    doc = Document()
    doc.add_paragraph(content)
    doc.save(filepath)

    return filepath
