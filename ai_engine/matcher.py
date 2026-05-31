from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(resume, job):
    if not job:
        return 0.0

    emb = model.encode([resume, job])
    return float(cosine_similarity([emb[0]], [emb[1]])[0][0])


def decide_application(score):
    if score > 0.06:
        return "APPLY"
    elif score > 0.03:
        return "REVIEW"
    else:
        return "SKIP"