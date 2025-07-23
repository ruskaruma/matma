#Code for api/routes.py

from fastapi import APIRouter, Query
from typing import Optional

router=APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "message": "Matma API is running"}


@router.get("/search")
def search(q: str=Query(..., description="Search query string")):
    # Placeholder logic (replace with vector search + rerank later)
    return {
        "query": q,
        "results": [
            {"id": 1, "title": "Example Paper 1", "score": 0.93},
            {"id": 2, "title": "Example Paper 2", "score": 0.89},
        ],
    }

@router.get("/")
def root():
    return {"message": "Welcome to Matma — Multimodal LLM Search API"}