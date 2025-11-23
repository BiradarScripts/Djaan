from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.search_engine import SearchEngine

app = FastAPI(title="Embedding Search Engine")

engine = SearchEngine()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    use_expansion: bool = False

@app.post("/search")
async def search_documents(request: SearchRequest):
    """
    Endpoint to search documents using vector similarity.
    """
    try:
        results = engine.search(request.query, request.top_k, request.use_expansion)
        return {"results": results} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh")
async def refresh_index():
    """Force re-check of document folder and update index."""
    engine.load_or_build_index()
    return {"status": "Index refreshed"}