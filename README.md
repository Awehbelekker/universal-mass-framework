# MASS — AI Intelligence Layer for Awake & DIGG

> The shared AI backbone powering **[Awake](https://awakesa.com)** (surf & outdoor store) and **[DIGG](https://digg.co.za)** (content platform).
> One natural-language API. Two businesses. Two superpowers.

[![CI/CD](https://github.com/Awehbelekker/universal-mass-framework/actions/workflows/deploy.yml/badge.svg)](https://github.com/Awehbelekker/universal-mass-framework/actions/workflows/deploy.yml)
![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![LangGraph](https://img.shields.io/badge/orchestration-LangGraph-orange)
![LiteLLM](https://img.shields.io/badge/llm-LiteLLM-green)

---

## What MASS actually is

MASS is not a generic framework — it is the dedicated AI layer wired into the Awake and DIGG ecosystem. Two real businesses, two audiences, one pipeline:

```
┌──────────────────────────────────────────────────────────────────┐
│                         MASS                                     │
│                                                                  │
│  END-USER (site visitor)          OWNER (you / your wife)        │
│  POST /search                     POST /intelligence             │
│  ─────────────────────            ──────────────────────         │
│  "do you have a beginner          "how does our 3/2mm wetsuit    │
│   wetsuit in a medium?"            price compare to O'Neill?"    │
│                                                                  │
│  → searches store catalog,        → scrapes competitor pages,    │
│    DIGG guides, live web            diffs against your prices,   │
│    → grounded answer                → price position + moat      │
└──────────────────────────────────────────────────────────────────┘
```

### For Awake customers
Ask anything in plain language — gear specs, wetsuit sizing, skill-level recommendations, surf lesson bookings — and get a grounded answer synthesised from the store catalog, DIGG content, and live web results.

### For the owner
Call `/intelligence` with any market question. MASS searches the web for competitors, scrapes their pages via Jina AI Reader, and returns a structured analysis: price position, your competitive moat, and a recommendation to hold, adjust, or reframe.

---

## Pipeline

```
receive_query
      │
classify_intent  ←  skipped when intent is pre-set (e.g. /intelligence)
      │
┌─────┴───────────┬──────────────┬─────────────────────┐
▼                 ▼              ▼                     ▼
retrieve      action_agent   web_search        competitive_intel
(pgvector)    (tool-calling) (Brave/Serper)    (Jina + LLM diff)
      │                 │              │                     │
      └────────┬─────────┘              └──────────┬──────────┘
               ▼                                   ▼
          synthesize ◄──────────────────────────────┘
               │
              END
```

| Intent | Node | Source |
|--------|------|--------|
| `search` / `product` / `order` | `retrieve` | Supabase pgvector |
| `web` | `web_search` | Brave Search → Serper → stub |
| `action` | `action_agent` | LiteLLM function-calling |
| `competitive` | `competitive_intel` | Jina scrape + LLM diff |

---

## Architecture

```
mass/
├── config.py        # Pydantic Settings — all env vars, safe defaults
├── models.py        # Pydantic request/response models (SearchRequest/Response)
├── graph.py         # LangGraph StateGraph — nodes + conditional routing
│   ├── receive_query_node       — cleans input, preserves pre-set intent
│   ├── classify_intent_node     — LiteLLM → one of 6 intent labels
│   ├── retrieve_node            — Supabase pgvector similarity search
│   ├── web_search_node          — Brave/Serper live web retrieval
│   ├── action_agent_node        — LiteLLM function-calling action planner
│   ├── competitive_intel_node   — Jina scrape + LLM competitive diff
│   └── synthesize_node          — LiteLLM grounded answer generation
├── main.py          # FastAPI — /health, /search (public), /intelligence (owner)
├── mcp_server.py    # MCP server — exposes mass_search as an AI tool
├── ingest.py        # Ingest DIGG (insights + pages) into pgvector
└── ingest_store.py  # Ingest Awake Store (products, categories, collections)
```

**Design principles:**
- **Model-agnostic** — swap `LITELLM_MODEL` to any LiteLLM-supported provider without touching code.
- **Graceful degradation** — every node has a stub fallback when API keys are absent (CI-safe, no credentials needed to run tests).
- **Intent bypass** — callers can pre-set `intent` in state; the classifier skips classification and routes directly.
- **Pluggable actions** — register new tools in `_ACTION_TOOLS` without modifying node logic.
- **MCP-compatible** — the full pipeline is a single `mass_search` MCP tool.

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

The API is live at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

### Run tests (no API keys required)
```bash
uv run pytest tests/ -v
```

---

## API reference

### `GET /health`
```json
{"status": "ok", "version": "0.1.0", "env": "development"}
```

### `POST /search` — customer-facing
```json
{
  "query": "what wetsuits do you have for cold water beginners?",
  "max_results": 5,
  "context": {"user_id": "u_123"}
}
```

**Response:**
```json
{
  "query": "what wetsuits do you have for cold water beginners?",
  "intent": "product",
  "results": [{"content": "...", "source": "supabase", "score": 0.87, "metadata": {}}],
  "synthesis": "For cold water beginners we recommend the 4/3mm Awake Flex...",
  "agent_trace": ["receive_query", "classify_intent", "retrieve", "synthesize"],
  "model": "gpt-4o-mini"
}
```

**Auth:** Pass `X-Api-Key: <MASS_API_KEY>` when `MASS_API_KEY` is set. Leave it empty in dev.

### `POST /intelligence` — owner-only
```json
{
  "query": "how does our 3/2mm wetsuit price compare to O'Neill and Billabong?"
}
```

**Response:**
```json
{
  "query": "how does our 3/2mm wetsuit price compare to O'Neill and Billabong?",
  "intent": "competitive",
  "results": [{
    "content": "**Price position:** Awake is R200–R400 cheaper than O'Neill...\n**Moat:** Local stock, skill-level guidance, and surf school bundle pricing.\n**Recommendation:** Hold price — your value proposition is service, not discount.",
    "source": "competitive-intel",
    "score": 1.0,
    "metadata": {"sources_scraped": 2, "competitor_urls": ["..."]}
  }],
  "synthesis": "You are well-positioned. Consider highlighting your bundle pricing...",
  "agent_trace": ["receive_query", "classify_intent", "competitive_intel", "synthesize"]
}
```

**Auth:** Same `X-Api-Key` as `/search`. In production always set `MASS_API_KEY` so end-users cannot call this endpoint.

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LITELLM_MODEL` | `gpt-4o-mini` | LLM for classification, action, synthesis, and competitive analysis |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model for pgvector retrieval |
| `OPENAI_API_KEY` | — | Or any other LiteLLM-supported provider key |
| `SUPABASE_URL` | — | Supabase project URL (enables pgvector retrieval) |
| `SUPABASE_SERVICE_KEY` | — | Supabase service role key |
| `BRAVE_API_KEY` | — | Brave Search API key (enables live web + competitive search) |
| `SERPER_API_KEY` | — | Serper API key (Brave fallback) |
| `JINA_API_KEY` | — | Jina AI Reader key for full-page competitor scraping (free tier works without key) |
| `MASS_API_KEY` | — | Shared auth token for `/search` and `/intelligence` |
| `LANGFUSE_PUBLIC_KEY` | — | Langfuse observability (optional) |
| `LANGFUSE_SECRET_KEY` | — | Langfuse observability (optional) |

---

## Ingestion

Populate the pgvector store before using retrieval-based queries:

```bash
# DIGG platform (insights + pages)
uv run python -m mass.ingest

# Awake Store (products, categories, collections)
uv run python -m mass.ingest_store

# Dry run (inspect without writing)
uv run python -m mass.ingest --dry-run
```

---

## Deployment

The repository ships with a **Cloud Run CI/CD pipeline** (`.github/workflows/deploy.yml`):

1. Every push to `main` runs the full test suite.
2. On passing tests, Cloud Build packages the Docker image.
3. Cloud Run deploys the new revision automatically.

Required GitHub secrets: `GCP_PROJECT_ID`, `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`.

---

## MCP integration

MASS exposes itself as an MCP tool for AI clients. Add to your `.mcp.json`:

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

The `mass_search` tool then appears in Claude Desktop, Cursor, and any other MCP-compatible client.

---

## Extending

### New action tools
Add an entry to `_ACTION_TOOLS` in `mass/graph.py` — the action agent picks it up automatically on the next `action` intent query:

```python
_ACTION_TOOLS.append({
    "type": "function",
    "function": {
        "name": "cancel_order",
        "description": "Cancel an existing customer order.",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
})
```

Read `tool_name` and `tool_args` from the result metadata to wire real execution.

### New data sources
Follow the pattern in `mass/ingest.py` and `mass/ingest_store.py` to add additional pgvector sources.

---

## Licence

MIT
