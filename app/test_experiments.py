from __future__ import annotations
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.db import get_session as real_get_session
from sqlalchemy.pool import StaticPool
from app.main import app

TESTURL = "sqlite://"
test_engine = create_engine(TESTURL, echo = False, connect_args = {"check_same_thread" : False}, poolclass = StaticPool)

def get_test_session():
    with Session(test_engine) as session:
        yield session

def create_test_db_tables():
    SQLModel.metadata.create_all(bind = test_engine)

app.dependency_overrides[real_get_session] = get_test_session

client = TestClient(app)

def setup_module(module):
    create_test_db_tables()

def create_user(email : str, full_name : str):
    payload = {"email" : email, "full_name" : full_name}
    response = client.post("/users", json=payload)
    assert response.status_code == 200
    return response.json()

def test_authorized_user_experiment():
    payload = {"name" : "test 1", "description" : "test desc 1"}
    user = create_user("user1@example.com", "User One")
    headers = {"X-User-ID" : str(user["id"])}
    response = client.post("/experiments", json = payload, headers = headers)
    payload = {"name" : "test 2", "description" : "test desc 2"}
    response = client.post("/experiments", json = payload, headers = headers)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["owner_id"] == user["id"]

    response=client.get("/experiments", headers = headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
    assert response.json()[0]["name"] == "test 1"
    assert response.json()[0]["owner_id"] == user["id"]

    response = client.get("experiments/1", headers = headers)
    assert response.status_code == 200
    assert response.json()["name"] == "test 1"
    assert response.json()["id"] == 1

    update_payload = {"description" : "update test desc 1"}
    response = client.patch("experiments/1", json = update_payload, headers = headers)
    assert response.status_code == 200
    assert response.json()["description"] == update_payload["description"]

    response = client.delete("experiments/1", headers = headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Experiment deleted"
    response = client.delete("experiments/1", headers = headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Experiment not found"



def test_unauthorized_user_experiment():
    payload = {"name" : "test 2", "description" : "test desc 2"}
    user = create_user("user2@example.com", "User Two")
    headers = {"X-User-ID" : str(user["id"])}

    response=client.get("/experiments", headers = headers)
    assert response.status_code == 200
    assert response.json() == []

    response = client.get("experiments/2", headers = headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not allowed to access this experiment"
    
    update_payload = {"description" : "update test desc 1"}
    response = client.patch("experiments/2", json = update_payload, headers = headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not allowed to access this experiment"

    response = client.delete("experiments/2", headers = headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not allowed to access this experiment"
    