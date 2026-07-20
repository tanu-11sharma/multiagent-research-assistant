"""
Orchestrates the planner -> searcher -> writer agent pipeline.

This is the "graph" of the multi-agent system: a linear pipeline where the
planner's output fans out into per-sub-question searcher calls, and all
searcher results feed into a single writer call. A LangGraph-based version
would model this same shape as a graph with a planner node, N parallel
searcher nodes, and a writer node -- the control flow here is identical,
just expressed as plain Python for a zero-dependency demo.
"""

from __future__ import annotations

from app.agents import PlannerAgent, SearcherAgent, WriterAgent, ResearchBrief


class ResearchOrchestrator:
    def __init__(self, planner=None, searcher=None, writer=None):
        self.planner = planner or PlannerAgent()
        self.searcher = searcher or SearcherAgent()
        self.writer = writer or WriterAgent()

    def run(self, question: str, max_sub_questions: int = 3, top_k: int = 2) -> ResearchBrief:
        sub_questions = self.planner.plan(question, max_sub_questions=max_sub_questions)

        evidence_by_subq = [
            self.searcher.search(sq.text, top_k=top_k) for sq in sub_questions
        ]

        return self.writer.write(question, sub_questions, evidence_by_subq)
