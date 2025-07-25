#Code for   model/text_encoder.py

from sentence_transformers import SentenceTransformer
import numpy as np

class TextEncoder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        """
        Encodes a list of texts into embeddings.
        """
        return self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
