from sentence_transformers import SentenceTransformer
from django.conf import settings

model = None

_model = None
def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_text(text: str):
    model = get_embedder()
    return model.encode([text], convert_to_numpy=True)[0]

