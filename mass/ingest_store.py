"""MASS content ingestion — Awakesa Store.

Reads product, category, and collection data from the Awakesa Store's
Supabase database, generates embeddings via LiteLLM, and upserts the
chunks into ``mass_documents`` for pgvector similarity search.

Usage
-----
::

    # Ingest all published products, categories, and collections
    uv run python -m mass.ingest_store

    # Dry run — print what would be ingested without writing
    uv run python -m mass.ingest_store --dry-run

Environment variables required
-------------------------------
    SUPABASE_URL            Awakesa Store Supabase URL
    SUPABASE_SERVICE_KEY    Awakesa Store service role key
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

HEADERS = {
    "apikey": settings.supabase_service_key,
    "Authorization": f"Bearer {settings.supabase_service_key}",
    "Content-Type": "application/json",
}
BASE = settings.supabase_url.rstrip("/") if settings.supabase_url else ""


async def _get(client: httpx.AsyncClient, table: str, select: str, filters: str = "") -> list[dict]:
    url = f"{BASE}/rest/v1/{table}?select={select}{filters}"
    r = await client.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


async def _embed(texts: list[str]) -> list[list[float]]:
    response = await litellm.aembedding(model=settings.embedding_model, input=texts)
    return [item["embedding"] for item in response.data]


def _chunk(text: str, max_chars: int = 1500, overlap: int = 200) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start: start + max_chars])
        start += max_chars - overlap
    return chunks


async def _upsert(client: httpx.AsyncClient, docs: list[dict], dry_run: bool) -> None:
    if dry_run:
        for d in docs:
            logger.info("[DRY RUN] source=%s  source_id=%s", d["source"], d["source_id"])
        return
    url = f"{BASE}/rest/v1/mass_documents"
    headers = {**HEADERS, "Prefer": "resolution=merge-duplicates"}
    r = await client.post(url, json=docs, headers=headers)
    r.raise_for_status()
    logger.info("Upserted %d documents.", len(docs))


async def ingest(dry_run: bool = False) -> None:
    """Main ingestion routine — embeds and stores Awakesa Store content."""
    if not settings.supabase_url or not settings.supabase_service_key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        docs: list[dict[str, Any]] = []
        texts: list[str] = []

        # ── Products ─────────────────────────────────────────────────────────
        products = await _get(
            client, "product",
            "id,title,subtitle,description,handle,status,material,skill_level,category_tag,collection_id",
            "&status=eq.published&deleted_at=is.null",
        )
        logger.info("Fetched %d published products.", len(products))
        for p in products:
            parts = filter(None, [p.get("title"), p.get("subtitle"), p.get("description")])
            full_text = " — ".join(parts)
            meta_tags = " ".join(filter(None, [p.get("material"), p.get("skill_level"), p.get("category_tag")]))
            if meta_tags:
                full_text += f"\n\nDetails: {meta_tags}"
            for i, chunk in enumerate(_chunk(full_text)):
                texts.append(chunk)
                docs.append({
                    "content": chunk,
                    "source": "product",
                    "source_id": f"{p['handle']}-{i}",
                    "metadata": {
                        "title": p["title"], "handle": p["handle"],
                        "skill_level": p.get("skill_level"), "category_tag": p.get("category_tag"),
                    },
                })

        # ── Categories ───────────────────────────────────────────────────────
        categories = await _get(
            client, "product_category",
            "id,name,handle,description",
            "&is_active=eq.true&is_internal=eq.false",
        )
        logger.info("Fetched %d active categories.", len(categories))
        for c in categories:
            full_text = " — ".join(filter(None, [c.get("name"), c.get("description")]))
            if not full_text:
                continue
            texts.append(full_text)
            docs.append({
                "content": full_text,
                "source": "product_category",
                "source_id": c["handle"],
                "metadata": {"name": c["name"], "handle": c["handle"]},
            })

        # ── Collections ──────────────────────────────────────────────────────
        collections = await _get(
            client, "product_collection",
            "id,title,handle",
            "&deleted_at=is.null",
        )
        logger.info("Fetched %d collections.", len(collections))
        for col in collections:
            full_text = col.get("title", "")
            if not full_text:
                continue
            texts.append(full_text)
            docs.append({
                "content": full_text,
                "source": "product_collection",
                "source_id": col["handle"],
                "metadata": {"title": col["title"], "handle": col["handle"]},
            })

        logger.info("Generating embeddings for %d chunks...", len(texts))
        embeddings = await _embed(texts)
        for doc, emb in zip(docs, embeddings):
            doc["embedding"] = emb

        await _upsert(client, docs, dry_run=dry_run)
        logger.info("Store ingestion complete — %d chunks stored.", len(docs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MASS store content ingestion")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")
    args = parser.parse_args()
    asyncio.run(ingest(dry_run=args.dry_run))

