import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.auth.dependencies import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.job import Job
from app.schemas import response
from unittest.mock import AsyncMock
from datetime import datetime , UTC

# Dummy user for testing
mock_user = User(
    id=1,
    full_name="Test User",
    email="test@example.com",
    hashed_password="hashed_password",
    is_active=True
)

async def override_get_current_user():
    return mock_user

# Override auth dependency
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_create_research_job_success():
    """
    Test successful enqueueing of a research job.
    """
    mock_db = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.add = MagicMock()
    
    # Override get_db dependency to return our mock DB session
    async def override_get_db():
        yield mock_db
        
    app.dependency_overrides[get_db] = override_get_db

    # Mock the Celery task .delay method
    with patch("app.api.v1.research.run_research_job.delay") as mock_delay:
        response = client.post(
            "/api/v1/research",
            json={"query": "test query"}
        )


        print("Status:", response.status_code)
        print("Response:", response.text)

        
        assert response.status_code == 202
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "queued"
        assert mock_delay.call_count == 1
        
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.asyncio
async def test_get_job_status():
    """
    Test retrieving job status.
    """
    # Create mock session
    mock_db = MagicMock()
    
    # Setup mock job in database
    mock_job = Job(
        job_id="test-job-uuid",
        user_id=1,
        query="test query",
        status="running",
        current_node="planner",
        iteration_count=1,
        sufficiency_score=0.5,
        coverage_metrics={"papers": 0.8},
        updated_at=datetime.utcnow()
                )
    
    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    # Mock DB query execution
    # For async sqlalchemy: await db.execute(...) returns a result
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_job
    
    # We must support the async call structure:
    # result = await db.execute(select(Job)...)
    # So we make db.execute an async mock returning mock_result
    async def async_execute(*args, **kwargs):
        return mock_result
        
    mock_db.execute = async_execute

    response = client.get("/api/v1/research/test-job-uuid/status")

    print("Status:", response.status_code)
    print("Response:", response.text)

    
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-uuid"
    assert data["status"] == "running"
    assert data["current_node"] == "planner"
    assert data["iteration_count"] == 1
    assert data["sufficiency_score"] == 0.5
    assert data["coverage_metrics"] == {"papers": 0.8}

    app.dependency_overrides.pop(get_db, None)
