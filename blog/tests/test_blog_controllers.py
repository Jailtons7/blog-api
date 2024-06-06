from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app import app
from db.connection import get_db, Base


DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False
    },
)
TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


client = TestClient(app=app)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)


def test_unauthorized():
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
