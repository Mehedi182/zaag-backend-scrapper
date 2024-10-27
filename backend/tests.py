import pytest
from config import settings
from fastapi import status
from httpx import AsyncClient
from main import app, get_db
from models import Base, User
from schemas import UserCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for testing
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)  # Create tables in the test database


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
def test_user():
    return UserCreate(username="mehedi", password="string")


@pytest.mark.asyncio
async def test_create_user(async_client, test_user):
    response = await async_client.post("/users/", json=test_user.dict())
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == test_user.username


@pytest.mark.asyncio
async def test_login_for_access_token(async_client, test_user):
    await async_client.post("/users/", json=test_user.dict())

    login_data = {"username": test_user.username, "password": test_user.password}
    response = await async_client.post("/token", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_read_users_me(async_client, test_user):
    token = await test_login_for_access_token(async_client, test_user)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get("/users/me/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == test_user.username


@pytest.mark.asyncio
async def test_create_sample(async_client, test_user):
    token = await test_login_for_access_token(async_client, test_user)
    headers = {"Authorization": f"Bearer {token}"}
    sample_data = {
        "name": "Sample Name",
        "tax_id": "12345",
        "gtdb_id": "GTDB123",
        "domain": "Bacteria",
        "abundance_score": 0.95,
        "relative_abundance": 0.85,
        "unique_matches": 10.0,
        "total_matches": 100.0,
        "unique_matches_frequency": 0.1,
        "reads_frequency": 50,
        "normalized_reads_frequency": 45,
        "go_id": "GO:0008150",
        "go_category": "Biological Process",
        "go_description": "Metabolic process",
        "copies_per_million": 5.0,
        "enzyme_id": "ENZ123",
        "pfam_id": "PF12345",
        "cazy_id": "CAZ123",
    }
    response = await async_client.post("/samples/", json=sample_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == sample_data["name"]


@pytest.mark.asyncio
async def test_read_samples(async_client, test_user):
    token = await test_login_for_access_token(async_client, test_user)
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.get("/samples/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_read_sample(async_client, test_user):
    token = await test_login_for_access_token(async_client, test_user)
    headers = {"Authorization": f"Bearer {token}"}
    sample_id = 1

    response = await async_client.get(f"/samples/{sample_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_sample(async_client, test_user):
    token = await test_login_for_access_token(async_client, test_user)
    headers = {"Authorization": f"Bearer {token}"}
    sample_id = 1
