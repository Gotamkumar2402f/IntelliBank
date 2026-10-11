from fastapi import APIRouter
from pydantic import BaseModel
from app.jarvis.brain import process_query

router = APIRouter(prefix="/jarvis", tags=["Jarvis AI"])

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@router.post("/ask", response_model=QueryResponse)
def ask_jarvis(request: QueryRequest):
    answer = process_query(request.query)
    return {"response": answer}