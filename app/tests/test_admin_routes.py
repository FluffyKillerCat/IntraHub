from app.tests.testconfig import TestingSessionLocal, engine
from app.models.user import User
from app.models.admins import Admins

from app.utilities.jwt import generate_access_token as create_access_token
from app.db.base import Base


def test_new_admin_route(client):

    db = TestingSessionLocal()

    admin_user = User(username="alice1", email="alic1ee11@example.com", password="fakeJ1291dqk182jdqw")
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    new_admin = User(username="bob1", email="alic111e11e@example.com", password="fakeJ1291dqk182jdqw")
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)


    org_admin = Admins(user_id=1, org_id="org_123", accepted_by="me")

    db.add(org_admin)
    db.commit()
    db.refresh(org_admin)
    db.close()

    token = create_access_token({"sub": "alice1"})
    response = client.post("/admins/", headers={"Authorization": f"Bearer {token}"}, json={"org_id": "org_123", "user_id": "bob1"})
    assert response.status_code == 200
    assert response.json()["user_id"] == 2
    assert response.json()["org_id"] == "org_123"
