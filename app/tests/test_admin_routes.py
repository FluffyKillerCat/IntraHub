import pytest
from app.tests.testconfig import TestingSessionLocal, engine
from app.models.user import User
from app.models.admins import Admins
from app.utilities.jwt import generate_access_token as create_access_token
from app.db.base import Base


@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def create_user(db, username, email, password="fakepass"):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_new_admin_route(client):
    db = TestingSessionLocal()
    admin_user = create_user(db, "alice_test1", "alice1@example.com")
    new_admin = create_user(db, "bob_test1", "bob1@example.com")

    org_admin = Admins(user_id=admin_user.id, org_id="org_123", accepted_by="me")
    db.add(org_admin)
    db.commit()

    token = create_access_token({"sub": admin_user.username})
    response = client.post(
        "/admins/",
        headers={"Authorization": f"Bearer {token}"},
        json={"org_id": "org_123", "user_id": "bob_test1"}
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == new_admin.id
    assert response.json()["org_id"] == "org_123"
    db.close()


def test_admin_route_unauthorized(client):
    response = client.post("/admins/", json={"org_id": "org_123", "user_id": "bob_test2"})
    assert response.status_code == 401


def test_admin_route_invalid_org_id(client):
    db = TestingSessionLocal()
    admin_user = create_user(db, "admin_test3", "admin3@example.com")
    new_admin = create_user(db, "bob_test3", "bob3@example.com")

    db.add(Admins(user_id=admin_user.id, org_id="org_wrong", accepted_by="me"))
    db.commit()

    token = create_access_token({"sub": admin_user.username})
    response = client.post(
        "/admins/",
        headers={"Authorization": f"Bearer {token}"},
        json={"org_id": "org_123", "user_id": "bob_test3"}
    )
    assert response.status_code == 401
    db.close()


def test_admin_route_user_not_exist(client):
    db = TestingSessionLocal()
    admin_user = create_user(db, "admin_test4", "admin4@example.com")

    db.add(Admins(user_id=admin_user.id, org_id="org_456", accepted_by="me"))
    db.commit()

    token = create_access_token({"sub": admin_user.username})
    response = client.post(
        "/admins/",
        headers={"Authorization": f"Bearer {token}"},
        json={"org_id": "org_456", "user_id": "ghost_user"}
    )
    assert response.status_code == 401
    db.close()


def test_non_admin_cannot_create_admin(client):
    db = TestingSessionLocal()
    non_admin_user = create_user(db, "charlie_test5", "charlie5@example.com")
    target_user = create_user(db, "target_test5", "target5@example.com")

    token = create_access_token({"sub": non_admin_user.username})
    response = client.post(
        "/admins/",
        headers={"Authorization": f"Bearer {token}"},
        json={"org_id": "org_789", "user_id": "target_test5"}
    )
    assert response.status_code == 401
    db.close()
