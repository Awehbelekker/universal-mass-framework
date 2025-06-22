import pytest
import sqlite3
import os
import bcrypt
import json
import subprocess
from datetime import datetime, timezone

# Set up a session-scoped fixture to set DATABASE_PATH to an absolute path before any test or app code runs
@pytest.fixture(scope="session", autouse=True)
def set_test_db_env():
    test_db_path = os.path.abspath(os.getenv("TEST_DB_PATH", "test_mass_framework.db"))
    os.environ["DATABASE_PATH"] = test_db_path
    yield

# Run migration first, then set up test data
@pytest.fixture(scope="session", autouse=True)
def run_schema_migration():
    test_db_path = os.path.abspath(os.getenv("TEST_DB_PATH", "test_mass_framework.db"))
    os.environ["DATABASE_PATH"] = test_db_path
    migration_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "migrate_db_schema.py"))
    subprocess.run(["python", migration_script], check=True, env=dict(os.environ, DATABASE_PATH=test_db_path))
    yield

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    db_path = os.environ["DATABASE_PATH"]
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Insert a valid default admin user if not exists
    admin_id = "admin-test-id"
    admin_username = "admin"
    admin_email = "admin@mass-framework.com"
    admin_password = "admin123"
    admin_role = "admin"
    admin_tenant = "default"
    admin_is_active = True
    admin_created_at = datetime.now(timezone.utc).isoformat()
    admin_metadata = {"created_by": "system", "is_default": True}
    admin_password_hash = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    c.execute("""
        INSERT OR IGNORE INTO users (id, username, email, password_hash, role, tenant_id, is_active, created_at, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        admin_id, admin_username, admin_email, admin_password_hash, admin_role, admin_tenant, admin_is_active, admin_created_at, json.dumps(admin_metadata)
    ))
    conn.commit()
    conn.close()
    yield
    # Optionally, clean up after tests
    if os.path.exists(db_path):
        os.remove(db_path)
