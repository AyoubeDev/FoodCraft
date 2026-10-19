import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=True)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

DB_URL = {
    "development": os.getenv("DB_URL_DEVELOPMENT"),
    "test": os.getenv("DB_URL_TEST"),
    "production": os.getenv("DB_URL_PRODUCTION")
}.get(ENVIRONMENT) or os.getenv("DATABASE_URL")

# SQLAlchemy defaults to psycopg2 for postgresql:// URLs.
# This project uses psycopg (v3), so we pin the driver when not specified.
if DB_URL and DB_URL.startswith("postgresql://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+psycopg://", 1)

if not DB_URL:
    raise RuntimeError(
        "Database URL is not configured. Set DATABASE_URL or DB_URL_DEVELOPMENT/DB_URL_TEST/DB_URL_PRODUCTION."
    )