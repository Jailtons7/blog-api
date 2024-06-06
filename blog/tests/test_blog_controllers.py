import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app import app
from db.connection import get_db, Base
from authentication.models import User


DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False
    },
)
TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="module")
def client():
    with TestClient(app=app) as c:
        yield c


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_user():
    password = "password"
    user = User(name="test", username="test", email="test@example.com")
    user.set_password(password=password)
    for db in override_get_db():
        db.add(user)
        db.commit()
        db.refresh(user)
    return {
        "username": user.email,
        "password": password,
    }


@pytest.fixture(scope="module")
def access_token(client, test_user):
    response = client.post("/auth/access-token", data=test_user)
    assert response.status_code == 201
    token = response.json()["access_token"]
    assert token is not None
    return token


def test_not_authenticated(client):
    protected_endpoints = [
        ("get", "/posts/"),
        ("get", "/posts/1"),
        ("post", "/posts/"),
        ("delete", "/posts/1"),
        ("put", "/posts/1"),
    ]
    for method, endpoint in protected_endpoints:
        response = getattr(client, method)(endpoint)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_add_posts(client, access_token):
    post_data = {
        "title": "test title",
        "body": "test body"
    }
    response = client.post(url="/posts", json=post_data, headers={"Authorization": f"Bearer {access_token}"})
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "test title"
    assert data["body"] == "test body"
    assert data["creator"]["id"] == 1
