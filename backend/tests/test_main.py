import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

# ------------------------------
# Use a separate test database
# ------------------------------
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_agriculture.db"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency to use test DB
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ------------------------------
# Create test tables
# ------------------------------
Base.metadata.drop_all(bind=engine)  # Ensure clean DB
Base.metadata.create_all(bind=engine)

# ------------------------------
# Test client
# ------------------------------
client = TestClient(app)

# ------------------------------
# Tests
# ------------------------------

def test_signup():
    response = client.post("/signup", json={"username": "testuser", "password": "1234"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_login():
    client.post("/signup", json={"username": "testuser2", "password": "1234"})
    response = client.post("/login", json={"username": "testuser2", "password": "1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_predict_file():
    file_data = {"file": ("testfile.txt", b"Hello World")}
    response = client.post("/predict", files=file_data)
    assert response.status_code == 200
    assert "File received" in response.json()["message"]
