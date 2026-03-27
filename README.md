# MASS — Multi-Agent Search System

> **"The jQuery of AI"** — a lightweight, universal orchestration framework that connects any query to the right specialist agent and synthesises a grounded answer.

[![CI/CD](https://github.com/Awehbelekker/universal-mass-framework/actions/workflows/deploy.yml/badge.svg)](https://github.com/Awehbelekker/universal-mass-framework/actions/workflows/deploy.yml)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![LangGraph](https://img.shields.io/badge/orchestration-LangGraph-orange)
![LiteLLM](https://img.shields.io/badge/llm-LiteLLM-green)

---

## What it does

MASS routes a natural-language query through a five-node LangGraph pipeline:

```
receive_query → classify_intent → ┬─ retrieve      ─┐
                                   ├─ web_search    ─┤→ synthesize → response
                                   └─ action_agent  ─┘
```

| Intent | Specialist node | What happens |
|--------|----------------|--------------|
| `search` / `product` / `order` | `retrieve` | Supabase pgvector similarity search |
| `web` | `web_search` | Brave Search API → Serper fallback → stub |
| `action` | `action_agent` | LiteLLM tool-calling → structured action |

Everything flows into `synthesize`, which asks the LLM to produce a grounded, concise answer using the retrieved context.

---

## Architecture

```
mass/
├── config.py        # Pydantic Settings — all env vars, safe defaults
├── models.py        # Pydantic request/response models + MASSState TypedDict
├── graph.py         # LangGraph StateGraph — all nodes + routing logic
│   ├── receive_query_node      — cleans and validates input
│   ├── classify_intent_node    — LiteLLM → one of 5 intent labels
│   ├── retrieve_node           — Supabase pgvector similarity search
│   ├── web_search_node         — Brave/Serper live web retrieval
│   ├── action_agent_node       — LiteLLM function-calling action planner
│   └── synthesize_node         — LiteLLM grounded answer generation
├── main.py          # FastAPI app — /health + /search endpoints
├── mcp_server.py    # MCP server — exposes mass_search as an AI tool
├── ingest.py        # Ingest DIGG (insights + pages) into pgvector
└── ingest_store.py  # Ingest Awakesa Store (products, categories, collections)
```

**Key design decisions:**
- **Model-agnostic** — swap `LITELLM_MODEL` from `gpt-4o-mini` to any provider without touching code.
- **Graceful degradation** — every specialist node has a stub fallback when API keys are absent (CI-safe).
- **Pluggable actions** — add entries to `_ACTION_TOOLS` in `graph.py` to extend the action agent without modifying node logic.
- **MCP-compatible** — the full pipeline is exposed as a single `mass_search` tool via the Model Context Protocol.

---

## Quick start

### Prerequisites
- Python 3.12+ and [uv](https://docs.astral.sh/uv/)
- An OpenAI (or compatible) API key for LiteLLM

```bash
git clone https://github.com/Awehbelekker/universal-mass-framework.git
cd universal-mass-framework
cp .env.example .env          # fill in at minimum OPENAI_API_KEY
uv sync
uv run uvicorn mass.main:app --reload
```

The API is now live at `http://localhost:8000`.

### Run tests
```bash
uv run pytest tests/ -v
```

---

## API reference

### `GET /health`
```json
{"status": "ok", "service": "MASS"}
```

### `POST /search`
```json
{
  "query": "what wetsuits do you have for beginners?",
  "max_results": 5,
  "context": {}
}
```

**Response:**
```json
{
  "query": "what wetsuits do you have for beginners?",
  "intent": "product",
  "results": [
    {
      "content": "...",
      "source": "product",
      "score": 0.87,
      "metadata": {"title": "...", "handle": "..."}
    }
  ],
  "synthesis": "We carry three beginner-friendly wetsuits...",
  "agent_trace": ["receive_query", "classify_intent", "retrieve", "synthesize"],
  "model": "gpt-4o-mini"
}
```

**Auth:** Set `MASS_API_KEY` in your env. When set, pass it as `X-API-Key: <key>` header.

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LITELLM_MODEL` | `gpt-4o-mini` | LLM for classification, action, and synthesis |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model for retrieval |
| `OPENAI_API_KEY` | — | Or any other LiteLLM-supported provider key |
| `SUPABASE_URL` | — | Supabase project URL (enables pgvector retrieval) |
| `SUPABASE_SERVICE_KEY` | — | Supabase service role key |
| `BRAVE_API_KEY` | — | Brave Search API key (enables live web search) |
| `SERPER_API_KEY` | — | Serper API key (Brave fallback) |
| `MASS_API_KEY` | — | Bearer token for `/search` endpoint auth |
| `LANGFUSE_PUBLIC_KEY` | — | Langfuse observability (optional) |
| `LANGFUSE_SECRET_KEY` | — | Langfuse observability (optional) |

---

## Ingestion

Populate the pgvector store before using retrieval-based queries:

```bash
# DIGG platform (insights + pages)
uv run python -m mass.ingest

# Awakesa Store (products, categories, collections)
uv run python -m mass.ingest_store

# Dry run (print without writing)
uv run python -m mass.ingest --dry-run
```

---

## Deployment

The repository ships with a **Cloud Run CI/CD pipeline** (`.github/workflows/deploy.yml`):

1. Every push to `main` runs the test suite.
2. On passing tests, Cloud Build packages the Docker image.
3. Cloud Run deploys the new revision.

Required GitHub secrets: `GCP_PROJECT_ID`, `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`.

---

## MCP integration

MASS exposes itself as an MCP tool. Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "mass": {
      "command": "uv",
      "args": ["run", "python", "-m", "mass.mcp_server"]
    }
  }
}
```

The `mass_search` tool then appears in any MCP-compatible AI client (Claude Desktop, Cursor, etc.).

---

## Extending the Action Agent

Register new capabilities by adding entries to `_ACTION_TOOLS` in `mass/graph.py`:

```python
_ACTION_TOOLS.append({
    "type": "function",
    "function": {
        "name": "cancel_order",
        "description": "Cancel an existing customer order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Order ID to cancel"},
            },
            "required": ["order_id"],
        },
    },
})
```

The action agent will automatically consider this tool on the next `action` intent query. Wire execution logic externally by reading `tool_name` and `tool_args` from the result metadata.

---

## Licence

MIT
