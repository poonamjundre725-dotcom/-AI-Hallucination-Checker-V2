from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def verify_answer(question, ai_answer, evidence):

    if not evidence.strip():

        return {
            "confidence": 0,
            "risk": 100,
            "verdict": "Hallucination",
            "reason": "No evidence found."
        }

    emb1 = model.encode([ai_answer])

    emb2 = model.encode([evidence])

    similarity = cosine_similarity(
        emb1,
        emb2
    )[0][0]

    confidence = round(
        similarity * 100
    )

    risk = 100 - confidence

    if confidence >= 80:

        verdict = "No Hallucination"

    elif confidence >= 60:

        verdict = "Partial Hallucination"

    else:

        verdict = "Hallucination"

    return {
        "confidence": confidence,
        "risk": risk,
        "verdict": verdict,
        "reason": f"Semantic similarity = {confidence}%"
    }