# Multi-Agent Research Assistant

A small, fully working demo of a **planner → searcher → writer** multi-agent
pipeline, exposed as a FastAPI endpoint. Given a research question, it:

1. **Plans** — breaks the question into a few focused sub-questions.
2. **Searches** — retrieves supporting evidence for each sub-question from a
   bundled synthetic knowledge base (keyword-overlap retrieval, no external
   API or network call).
3. **Writes** — synthesizes the retrieved evidence into a short, cited
   research brief.

## Why this is relevant

This mirrors the multi-agent orchestration pattern popularized by frameworks
like LangGraph: a planner node fans out work to worker/searcher nodes, whose
outputs are merged by a final writer/critic node. The pipeline shape here is
identical to a LangGraph graph (planner node → N searcher nodes → writer
node); it's implemented in plain Python so the demo runs end-to-end with
**zero external API keys and zero network calls**.

This is a demo / learning project, **not** a production research tool. All
data is synthetic sample text bundled in `app/corpus.py`.

## Project structure

```
app/
  corpus.py        # synthetic sample knowledge base (8 short documents)
  agents.py         # PlannerAgent, SearcherAgent, WriterAgent
  orchestrator.py    # wires the three agents into a pipeline
  main.py            # FastAPI app exposing POST /research
tests/
  test_pipeline.py   # unit + end-to-end tests for each agent and the pipeline
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Example usage

```bash
curl -s -X POST http://127.0.0.1:8000/research \
  -H "Content-Type: application/json" \
  -d '{"question": "How does retrieval-augmented generation work?"}' \
  | python3 -m json.tool
```

Example response shape:

```json
{
  "question": "How does retrieval-augmented generation work?",
  "sub_questions": [
    {"text": "What is retrieval-augmented generation work?"},
    {"text": "Why does retrieval-augmented generation work matter in AI systems today?"},
    {"text": "What are common patterns or trade-offs for retrieval-augmented generation work?"}
  ],
  "sections": [
    {
      "sub_question": "What is retrieval-augmented generation work?",
      "answer": "Retrieval-Augmented Generation (RAG) combines a retriever...",
      "citations": ["doc-1"]
    }
  ],
  "sources": ["doc-1", "doc-7"]
}
```

You can also run it as a plain CLI/script without a web server:

```bash
python3 -c "
from app.orchestrator import ResearchOrchestrator
brief = ResearchOrchestrator().run('What is agentic AI?')
for section in brief.sections:
    print('-', section['sub_question'])
    print(' ', section['answer'])
"
```

## Tests

```bash
pytest -v
```

## Docker (optional)

```bash
docker build -t multiagent-research-assistant .
docker run -p 8000:8000 multiagent-research-assistant
```

## Notes / limitations

- Retrieval uses simple normalized keyword-overlap scoring against a small
  bundled corpus — good enough to demonstrate the pipeline shape, not a
  production-grade retriever (no embeddings, no vector DB).
- No real web search, no external LLM calls, no API keys required to run the
  core demo.
