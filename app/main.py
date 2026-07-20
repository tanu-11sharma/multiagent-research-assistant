"""
FastAPI wrapper exposing the planner -> searcher -> writer pipeline as a
single HTTP endpoint. Run locally with:

    uvicorn app.main:app --reload

Then:

    curl -s -X POST http://127.0.0.1:8000/research \
      -H "Content-Type: application/json" \
      -d '{"question": "How does retrieval-augmented generation work?"}' | python3 -m json.tool
"""

from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.orchestrator import ResearchOrchestrator

app = FastAPI(
    title="Multi-Agent Research Assistant",
    description=(
        "Demo LangGraph-style planner -> searcher -> writer pipeline that "
        "produces a short, cited research brief from a bundled synthetic "
        "knowledge base. No external API keys or network calls required."
    ),
    version="0.1.0",
)

_orchestrator = ResearchOrchestrator()


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=3, description="Research question to investigate")
    max_sub_questions: int = Field(3, ge=1, le=3)
    top_k: int = Field(2, ge=1, le=5)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(req: ResearchRequest):
    brief = _orchestrator.run(
        req.question,
        max_sub_questions=req.max_sub_questions,
        top_k=req.top_k,
    )
    return asdict(brief)
