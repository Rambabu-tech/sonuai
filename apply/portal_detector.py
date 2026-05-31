def detect_portal(url: str) -> str:
    url = url.lower()
    if "linkedin.com/jobs" in url:
        return "linkedin"
    if "greenhouse.io" in url:
        return "greenhouse"
    return "manual"
