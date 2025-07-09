# test_admin_routes.py
from app.tests.testconfig import TestingSessionLocal, engine
from app.models.user import User
from app.utilities.jwt import generate_access_token as create_access_token
from app.db.base import Base
# --- Test /me route ---
def test_me_route(client):
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    test_user = User(username="alice", email="alicee@example.com", password="fakeJ1291dqk182jdqw")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()

    token = create_access_token({"sub": "alice"})

    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["username"] == "alice"


# --- Test DELETE user (authorized) ---
def test_delete_user_success(client):
    db = TestingSessionLocal()
    test_user = User(username="bob", email="bob@example.com", password="123")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()

    token = create_access_token({"sub": "bob"})
    response = client.delete("/users/users/bob", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

# --- Test DELETE user (forbidden) ---
"""def test_delete_user_forbidden(client):
    db = TestingSessionLocal()
    db.add_all([
        User(username="john", email="john@example.com", password="123"),
        User(username="doe", email="doe@example.com", password="123")
    ])
    db.commit()
    db.close()

    token = create_access_token({"sub": "john"})
    response = client.delete("/users/doe", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403"""

# --- Cleanup after module ---
"""def teardown_module(module):
    Base.metadata.drop_all(bind=engine)"""
