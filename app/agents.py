"""
Planner -> Searcher -> Writer multi-agent pipeline.

Each "agent" here is a small, independently-testable Python class with a
single responsibility, orchestrated in sequence by orchestrator.py. This
mirrors the node-based planner/worker/writer pattern popularized by
frameworks like LangGraph, implemented here with plain Python + a
lightweight keyword-overlap retriever so the whole demo runs with zero
external API keys and zero network calls.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

from app.corpus import DOCUMENTS

_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "of", "in", "on", "to",
    "for", "and", "or", "how", "what", "why", "does", "do", "with", "vs",
    "about", "compare", "explain", "between",
}


def _tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in _STOPWORDS and len(w) > 2]


@dataclass
class SubQuestion:
    text: str


@dataclass
class Evidence:
    doc_id: str
    title: str
    snippet: str
    score: float


@dataclass
class ResearchBrief:
    question: str
    sub_questions: List[SubQuestion]
    sections: List[dict] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)


class PlannerAgent:
    """Decomposes a broad research question into focused sub-questions."""

    #: template angles used to decompose any topic into sub-questions
    _ANGLES = [
        "What is {topic}?",
        "Why does {topic} matter in AI systems today?",
        "What are common patterns or trade-offs for {topic}?",
    ]

    _LEADING_PATTERNS = [
        r"^how\s+does\s+",
        r"^how\s+do\s+",
        r"^what\s+is\s+",
        r"^what\s+are\s+",
        r"^why\s+does\s+",
        r"^why\s+do\s+",
        r"^explain\s+",
    ]

    def _extract_topic(self, question: str) -> str:
        topic = question.strip().rstrip("?").strip()
        lowered = topic.lower()
        for pattern in self._LEADING_PATTERNS:
            match = re.match(pattern, lowered)
            if match:
                topic = topic[match.end():]
                break
        return topic.strip() or question.strip().rstrip("?")

    def plan(self, question: str, max_sub_questions: int = 3) -> List[SubQuestion]:
        if not question or not question.strip():
            raise ValueError("question must not be empty")
        topic = self._extract_topic(question)
        angles = self._ANGLES[:max_sub_questions]
        return [SubQuestion(text=angle.format(topic=topic)) for angle in angles]


class SearcherAgent:
    """Retrieves supporting evidence for a sub-question from the corpus.

    Uses simple normalized keyword-overlap scoring (no external dependency,
    no network call) -- enough to demonstrate the retrieval step of a RAG-
    style pipeline against the bundled synthetic corpus.
    """

    def __init__(self, documents=None):
        self.documents = documents if documents is not None else DOCUMENTS

    def search(self, query: str, top_k: int = 2) -> List[Evidence]:
        query_terms = set(_tokenize(query))
        if not query_terms:
            return []

        scored: List[Evidence] = []
        for doc in self.documents:
            doc_terms = _tokenize(doc["title"] + " " + doc["text"])
            if not doc_terms:
                continue
            overlap = query_terms.intersection(doc_terms)
            score = len(overlap) / len(query_terms)
            if score > 0:
                snippet = doc["text"][:220].rsplit(" ", 1)[0] + "..."
                scored.append(
                    Evidence(
                        doc_id=doc["id"],
                        title=doc["title"],
                        snippet=snippet,
                        score=round(score, 3),
                    )
                )

        scored.sort(key=lambda e: e.score, reverse=True)
        return scored[:top_k]


class WriterAgent:
    """Synthesizes retrieved evidence into a short cited research brief."""

    def write(self, question: str, sub_questions: List[SubQuestion],
              evidence_by_subq: List[List[Evidence]]) -> ResearchBrief:
        sections = []
        all_sources: List[str] = []

        for subq, evidence_list in zip(sub_questions, evidence_by_subq):
            if not evidence_list:
                sections.append(
                    {
                        "sub_question": subq.text,
                        "answer": "No supporting evidence found in the knowledge base.",
                        "citations": [],
                    }
                )
                continue

            answer_parts = [e.snippet for e in evidence_list]
            citations = [e.doc_id for e in evidence_list]
            all_sources.extend(citations)
            sections.append(
                {
                    "sub_question": subq.text,
                    "answer": " ".join(answer_parts),
                    "citations": citations,
                }
            )

        # de-duplicate sources while preserving order
        seen = set()
        unique_sources = []
        for s in all_sources:
            if s not in seen:
                seen.add(s)
                unique_sources.append(s)

        return ResearchBrief(
            question=question,
            sub_questions=sub_questions,
            sections=sections,
            sources=unique_sources,
        )
