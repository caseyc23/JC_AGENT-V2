"""Optional FastAPI app exposing third-party docs search.

Start with: `uvicorn jc.third_party_api:app --port 8001`
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from .third_party_index import search

app = FastAPI(title="JC Third-Party Index API")


class SearchResult(BaseModel):
    name: str
    path: str
    score: int


@app.get("/third-party/search", response_model=List[SearchResult])
def api_search(q: str, top: int = 5):
    if not q:
        raise HTTPException(status_code=400, detail="q parameter required")
    results = search(q)[:top]
    return results
