# Agentic AI Workflow

An independent Python reference workflow for routing a question to approved tools and returning a traceable answer. It demonstrates typed state, bounded execution, tool allowlisting, error handling, and source attribution. It does **not** contain employer code or claim production deployment.

## Run

```bash
python -m agentic_workflow.cli "What is the refund policy?"
python -m agentic_workflow.cli "How many orders are open?"
python -m unittest discover -s tests -v
```

The examples use synthetic knowledge and an in-memory SQLite table. `Workflow.run` routes a request, executes at most one tool, and returns `answer`, `tool`, `evidence`, and `status`. Unsupported questions abstain. SQL is selected from a fixed query allowlist; user text never becomes SQL. No LLM or external API is used in this baseline.

## Architecture

`request → keyword router → approved knowledge/SQL tool → evidence check → answer`

This bounded deterministic baseline is useful for testing tool contracts before integrating a model planner. Future work: LangGraph orchestration, model tool calling, approval for mutating actions, tracing, and adversarial evaluation. These are not currently implemented.
