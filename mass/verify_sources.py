"""Pluggable ground-truth sources for action verification.

The contract check (`ContractVerifier`) says an action is *well-formed*. A **lookup** check says its
*claim is actually true* — e.g. the `record_id` the LLM extracted really exists, or a price it set
matches the price table. Those need a source of truth, which is app-specific — so it's pluggable.

Register real DB-backed lookups in production via `register_records` / `register_prices` (or swap
these for adapters). Empty by default → the lookup step is skipped and verification stays
contract-only, so nothing changes until you wire a source.
"""
from __future__ import annotations

from typing import Any

_RECORDS: dict[tuple[str, str], dict] = {}   # (record_type, record_id) -> record
_PRICES: dict[str, float] = {}               # sku -> price


def register_records(records: dict[tuple[str, str], dict]) -> None:
    _RECORDS.update(records)


def register_prices(prices: dict[str, float]) -> None:
    _PRICES.update(prices)


def clear() -> None:
    _RECORDS.clear()
    _PRICES.clear()


def has_sources() -> bool:
    return bool(_RECORDS or _PRICES)


def lookup_record(record_type: str, record_id: str) -> dict | None:
    return _RECORDS.get((record_type, record_id))


def lookup_price(sku: str) -> Any:
    return _PRICES.get(sku)
