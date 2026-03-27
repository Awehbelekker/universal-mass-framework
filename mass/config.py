"""Runtime configuration via environment variables.

All settings have safe defaults so the service starts locally without any
environment configuration. Production values are injected as Cloud Run
environment variables (see .github/workflows/deploy.yml).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Runtime environment identifier
    mass_env: str = "development"

    # API key for authenticating callers (leave empty to disable auth in dev)
    mass_api_key: str = ""

    # GCP identifiers — populated automatically on Cloud Run
    gcp_project_id: str = ""
    gcp_region: str = "us-central1"

    # LLM routing — wired to LiteLLM
    litellm_model: str = "gpt-4o-mini"

    # Embedding model — used by retrieve_node to vectorise queries
    # Must match the dimension used when documents were ingested (1536 for
    # text-embedding-3-small).
    embedding_model: str = "text-embedding-3-small"

    # Supabase — vector store for pgvector retrieval.
    # Leave empty to fall back to the stub retrieve_node (safe for CI / local dev).
    supabase_url: str = ""
    supabase_service_key: str = ""

    # Web Search Agent (Move 4) — Brave is tried first, Serper as fallback.
    # Leave both empty to use the stub web_search_node (safe for CI / local dev).
    brave_api_key: str = ""
    serper_api_key: str = ""

    # Jina AI Reader — used by competitive_intel_node to scrape competitor pages
    # into LLM-ready markdown. Works without a key (rate-limited free tier);
    # supply a key for higher rate limits: https://jina.ai/
    jina_api_key: str = ""

    # Observability — wired to Langfuse
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Singleton settings instance imported by all modules
settings = Settings()

