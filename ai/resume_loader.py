def load_resume_text(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return f.read()
    except:
        return ""
