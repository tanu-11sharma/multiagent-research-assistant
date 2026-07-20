"""
Synthetic sample knowledge base for the research assistant demo.

All documents below are hand-written, self-contained sample text about
AI agent design patterns. No external data, scraping, or API keys are
used anywhere in this project. This is a demo dataset only.
"""

DOCUMENTS = [
    {
        "id": "doc-1",
        "title": "Retrieval-Augmented Generation (RAG) Basics",
        "text": (
            "Retrieval-Augmented Generation (RAG) combines a retriever, which "
            "fetches relevant passages from a document store, with a generator "
            "that composes an answer grounded in those passages. RAG reduces "
            "hallucination by forcing the model to cite retrieved evidence "
            "rather than rely purely on parametric memory. Common retrievers "
            "include TF-IDF, BM25, and dense embedding search."
        ),
    },
    {
        "id": "doc-2",
        "title": "Agentic AI and Tool Use",
        "text": (
            "Agentic AI refers to systems where a language model plans a "
            "sequence of actions, calls external tools or APIs, observes the "
            "results, and iterates until a goal is reached. Agentic loops "
            "typically involve a planning step, an action/tool-call step, and "
            "an observation step, repeated until a stopping condition is met."
        ),
    },
    {
        "id": "doc-3",
        "title": "Multi-Agent Orchestration Patterns",
        "text": (
            "Multi-agent systems split a task across specialized agents, such "
            "as a planner that decomposes a goal into sub-tasks, a worker or "
            "searcher agent that gathers information, and a writer or critic "
            "agent that synthesizes the final output. Frameworks like "
            "LangGraph model this as a directed graph of nodes, where each "
            "node is an agent step and edges define the control flow between "
            "them."
        ),
    },
    {
        "id": "doc-4",
        "title": "Model Context Protocol (MCP)",
        "text": (
            "The Model Context Protocol (MCP) standardizes how AI applications "
            "connect language models to external tools, data sources, and "
            "services. An MCP server exposes a set of tools with typed "
            "schemas; an MCP client (often an agent) discovers and calls those "
            "tools during its reasoning loop. This decouples tool "
            "implementations from any single model provider."
        ),
    },
    {
        "id": "doc-5",
        "title": "Evaluating Agent and RAG Pipelines",
        "text": (
            "Evaluating agentic and RAG systems typically covers retrieval "
            "quality (precision/recall of retrieved passages), answer "
            "faithfulness (does the answer only state what evidence supports), "
            "and task completion rate for multi-step agents. Lightweight eval "
            "harnesses run a fixed set of sample queries against the pipeline "
            "and check outputs against expected criteria."
        ),
    },
    {
        "id": "doc-6",
        "title": "Guardrails for AI Applications",
        "text": (
            "Guardrails constrain what an AI system is allowed to input and "
            "output. Input guardrails filter or redact sensitive content "
            "before it reaches a model; output guardrails validate or rewrite "
            "generated text, for example blocking unsafe instructions or "
            "redacting personally identifiable information (PII) before a "
            "response is returned to a user."
        ),
    },
    {
        "id": "doc-7",
        "title": "Planner-Searcher-Writer Pipelines",
        "text": (
            "A common lightweight multi-agent pattern for research assistants "
            "is planner-searcher-writer: the planner decomposes a broad "
            "question into a handful of focused sub-questions, the searcher "
            "retrieves supporting evidence for each sub-question from a "
            "knowledge base, and the writer synthesizes the retrieved evidence "
            "into a short, cited brief that directly answers the original "
            "question."
        ),
    },
    {
        "id": "doc-8",
        "title": "Why Small Working Demos Matter",
        "text": (
            "Small, end-to-end working demos are useful for validating an "
            "architecture pattern before committing to a larger build. A demo "
            "that runs entirely on synthetic data, with no external API keys "
            "required, can still exercise the full pipeline shape -- "
            "planning, retrieval, synthesis -- that a production system would "
            "use, just against a smaller and simpler dataset."
        ),
    },
]
