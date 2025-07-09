# conftest.py
import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db
from app.tests.testconfig import TestingSessionLocal, engine
import app.api.user_routes as user_routes
from app.db.base import Base
# ✅ Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[user_routes.get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # ✅ Make sure test.db exists before creating tables
    with open("test.db", "a"):
        pass

    # ✅ Create tables for all models
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        Base.metadata.create_all(bind=engine)
        yield c

    # ✅ Drop all tables after test module
    #Base.metadata.drop_all(bind=engine)

# ✅ Optional: delete file completely after all tests
def pytest_sessionfinish(session, exitstatus):
    if os.path.exists("test.db"):
        os.remove("test.db")
