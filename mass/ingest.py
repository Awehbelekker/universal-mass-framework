"""MASS content ingestion utility.

Reads content from DIGG's Supabase tables (insights, pages), generates
embeddings via LiteLLM, and upserts them into ``mass_documents`` for
pgvector similarity search.

Usage
-----
::

    # Ingest all published insights and pages
    uv run python -m mass.ingest

    # Dry run (print what would be ingested, no writes)
    uv run python -m mass.ingest --dry-run

Environment variables required
-------------------------------
    SUPABASE_URL            e.g. https://xrthcowlcohqlfwurryz.supabase.co
    SUPABASE_SERVICE_KEY    Supabase service role key (not the anon key)
    OPENAI_API_KEY          Required for text-embedding-3-small
"""

from __future__ import annotations

import argparse
import asyncio
import logging
from typing import Any

import httpx
import litellm

from mass.config import settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SUPABASE_HEADERS = {
    "apikey": settings.supabase_service_key,
    "Authorization": f"Bearer {settings.supabase_service_key}",
    "Content-Type": "application/json",
}
BASE_URL = settings.supabase_url.rstrip("/") if settings.supabase_url else ""


async def _fetch_table(client: httpx.AsyncClient, table: str, select: str) -> list[dict]:
    """Fetch rows from a Supabase table via REST."""
    url = f"{BASE_URL}/rest/v1/{table}?select={select}&published=eq.true"
    resp = await client.get(url, headers=SUPABASE_HEADERS)
    resp.raise_for_status()
    return resp.json()


async def _embed(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of texts using LiteLLM."""
    response = await litellm.aembedding(model=settings.embedding_model, input=texts)
    return [item["embedding"] for item in response.data]


async def _upsert_documents(
    client: httpx.AsyncClient, docs: list[dict[str, Any]], dry_run: bool
) -> None:
    """Upsert a batch of documents into mass_documents."""
    if dry_run:
        for doc in docs:
            logger.info("[DRY RUN] Would upsert: source=%s source_id=%s", doc["source"], doc["source_id"])
        return

    url = f"{BASE_URL}/rest/v1/mass_documents"
    headers = {**SUPABASE_HEADERS, "Prefer": "resolution=merge-duplicates"}
    resp = await client.post(url, json=docs, headers=headers)
    resp.raise_for_status()
    logger.info("Upserted %d documents.", len(docs))


def _chunk_text(text: str, max_chars: int = 1500) -> list[str]:
    """Split long text into overlapping chunks for better retrieval."""
    if len(text) <= max_chars:
        return [text]
    chunks, start = [], 0
    overlap = 200
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start += max_chars - overlap
    return chunks


async def ingest(dry_run: bool = False) -> None:
    """Main ingestion routine — embeds and stores all DIGG content."""
    if not settings.supabase_url or not settings.supabase_service_key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # ── Insights ─────────────────────────────────────────────────────────
        insights = await _fetch_table(client, "insights", "id,slug,title,body")
        logger.info("Fetched %d published insights.", len(insights))

        docs: list[dict[str, Any]] = []
        texts: list[str] = []

        for row in insights:
            body = row.get("body") or ""
            for i, chunk in enumerate(_chunk_text(f"{row['title']}\n\n{body}")):
                texts.append(chunk)
                docs.append({
                    "content": chunk,
                    "source": "insights",
                    "source_id": f"{row['slug']}-{i}",
                    "metadata": {"title": row["title"], "slug": row["slug"]},
                })

        # ── Pages ─────────────────────────────────────────────────────────────
        pages = await _fetch_table(client, "pages", "id,slug,title,meta_description,content_html")
        logger.info("Fetched %d published pages.", len(pages))

        for row in pages:
            text_content = " ".join(filter(None, [
                row.get("title"), row.get("meta_description"), row.get("content_html")
            ]))
            for i, chunk in enumerate(_chunk_text(text_content)):
                texts.append(chunk)
                docs.append({
                    "content": chunk,
                    "source": "pages",
                    "source_id": f"{row['slug']}-{i}",
                    "metadata": {"title": row["title"], "slug": row["slug"]},
                })

        logger.info("Generating embeddings for %d chunks...", len(texts))
        embeddings = await _embed(texts)

        for doc, emb in zip(docs, embeddings):
            doc["embedding"] = emb

        await _upsert_documents(client, docs, dry_run=dry_run)
        logger.info("Ingestion complete. %d chunks stored.", len(docs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MASS content ingestion")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be ingested without writing")
    args = parser.parse_args()
    asyncio.run(ingest(dry_run=args.dry_run))

