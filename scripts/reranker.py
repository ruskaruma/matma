from sentence_transformers import CrossEncoder
from typing import List, Tuple

# Choose a lightweight cross-encoder reranker
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, passages: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    # Create pairs of (query, passage)
    pairs = [(query, passage) for passage in passages]
    scores = reranker_model.predict(pairs)
    
    # Combine passages and scores
    scored_passages = list(zip(passages, scores))
    
    # Sort by score descending
    ranked = sorted(scored_passages, key=lambda x: x[1], reverse=True)
    
    return ranked[:top_k]
