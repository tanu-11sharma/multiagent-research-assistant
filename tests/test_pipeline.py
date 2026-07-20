import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents import PlannerAgent, SearcherAgent, WriterAgent
from app.orchestrator import ResearchOrchestrator


def test_planner_produces_expected_number_of_sub_questions():
    planner = PlannerAgent()
    subqs = planner.plan("retrieval-augmented generation", max_sub_questions=3)
    assert len(subqs) == 3
    assert all(sq.text.strip() for sq in subqs)


def test_planner_rejects_empty_question():
    planner = PlannerAgent()
    try:
        planner.plan("   ")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_searcher_finds_relevant_document_for_rag_query():
    searcher = SearcherAgent()
    results = searcher.search("What is retrieval-augmented generation?", top_k=2)
    assert len(results) >= 1
    assert any(r.doc_id == "doc-1" for r in results)


def test_searcher_returns_empty_for_nonsense_query():
    searcher = SearcherAgent()
    results = searcher.search("the a of", top_k=2)
    assert results == []


def test_writer_produces_sections_and_sources():
    planner = PlannerAgent()
    searcher = SearcherAgent()
    writer = WriterAgent()

    subqs = planner.plan("multi-agent orchestration", max_sub_questions=2)
    evidence = [searcher.search(sq.text, top_k=2) for sq in subqs]
    brief = writer.write("multi-agent orchestration", subqs, evidence)

    assert brief.question == "multi-agent orchestration"
    assert len(brief.sections) == 2
    assert isinstance(brief.sources, list)


def test_end_to_end_orchestrator_run():
    orchestrator = ResearchOrchestrator()
    brief = orchestrator.run("How does the Model Context Protocol work?", max_sub_questions=3, top_k=2)

    assert brief.question.startswith("How does")
    assert len(brief.sub_questions) == 3
    assert len(brief.sections) == 3
    # at least one section should have found evidence about MCP
    assert any("doc-4" in section["citations"] for section in brief.sections)
    assert "doc-4" in brief.sources


def test_end_to_end_orchestrator_handles_offtopic_gracefully():
    orchestrator = ResearchOrchestrator()
    brief = orchestrator.run("xyzzy plugh quux", max_sub_questions=1, top_k=2)
    assert len(brief.sections) == 1
    # no crash even when no evidence is found
    assert brief.sections[0]["citations"] == [] or isinstance(brief.sections[0]["citations"], list)
