from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
import hashlib

from scripts.rag_pipeline import generate_answer
from scripts.faiss_utils import search_faiss_index

# Basic in-memory cache
query_cache = {}

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

@router.get("/")
def root():
    return {"message": "Welcome to Matma — Multimodal LLM Search API"}

@router.post("/rag-search")
def rag_search(query: SearchQuery):
    q = query.query.strip()

    # Hash query for cache key
    key = hashlib.sha256(q.encode()).hexdigest()

    # Check cache
    if key in query_cache:
        return query_cache[key]

    # Search and generate response
    search_results = search_faiss_index(q)
    response = generate_answer(q, search_results)

    # Cache the result
    query_cache[key] = response

    return response
