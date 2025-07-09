# app/db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Get the absolute test DB path to avoid permission issues
TEST_DB_PATH = os.path.abspath("test.db")

# 2. Explicit environment check (case-sensitive)
def get_database_url():
    if os.environ.get("TESTING") == "1":  # Strict check
        print("✅ USING SQLITE FOR TESTS")  # Debug confirmation
        return f"sqlite:///{TEST_DB_PATH}"  # Absolute path
    print("⚠️ USING POSTGRESQL (PROD/DEV)")
    return os.getenv("DATABASE_URL")  # Your PostgreSQL URL

# 3. Force new engine creation
engine = create_engine(
    get_database_url(),
    connect_args={"check_same_thread": False} if "sqlite" in get_database_url() else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
