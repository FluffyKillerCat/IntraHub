# testconfig.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False, "uri": True}
)

TestingSessionLocal = sessionmaker(bind=engine)

# ❌ DO NOT call create_all here — move it to conftest.py
