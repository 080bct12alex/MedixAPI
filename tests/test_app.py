
import pytest
import asyncio
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from unittest.mock import patch

from beanie import init_beanie

from app import app
from services.auth import get_current_doctor
from models.doctor import Doctor
from models.patient import Patient

# Fixture to set up a mock database and test client for each test
@pytest.fixture
def client():
    # Use an in-memory mock database for tests
    mock_client = AsyncMongoMockClient()

    # Asynchronously initialize beanie with the mock database
    async def init_test_db():
        await init_beanie(
            database=mock_client.get_database(name="test_db"),
            document_models=[Doctor, Patient],
        )

    # Run the async initialization
    asyncio.run(init_test_db())

    # Mock the authentication dependency to always return a test doctor
    app.dependency_overrides[get_current_doctor] = lambda: "test_doctor"
    
    # Provide the TestClient to the tests
    yield TestClient(app)
    
    # Clean up the dependency override after the test is done
    app.dependency_overrides = {}


# Mark tests that use async database operations with @pytest.mark.asyncio
def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Patient Management System API'}


def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert response.json() == {'message': 'A fully functional API to manage your patient records'}


@pytest.mark.asyncio
async def test_register_doctor_success(client):
    # Patch the password hashing function as we don't need to test its logic
    with patch("routers.auth.get_password_hash") as mock_hash:
        mock_hash.return_value = "hashed_password"
        response = client.post("/auth/register", json={"username": "testuser", "password": "testpassword"})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Doctor registered successfully"}
        
        # Verify the doctor was actually created in the mock database
        doctor = await Doctor.find_one(Doctor.username == "testuser")
        assert doctor is not None
        assert doctor.password == "hashed_password"


@pytest.mark.asyncio
async def test_register_doctor_already_exists(client):
    # Pre-populate the database with a doctor
    await Doctor(username="testuser", password="hashed_password").create()
    
    response = client.post("/auth/register", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


@pytest.mark.asyncio
async def test_view_patients(client):
    # Pre-populate the database with patients
    await Patient(id="P001", name="Alice", city="A", age=30, gender="female", height=1.6, weight=60, doctor_id="test_doctor").create()
    await Patient(id="P002", name="Bob", city="B", age=40, gender="male", height=1.8, weight=80, doctor_id="test_doctor").create()
    await Patient(id="P003", name="Charlie", city="C", age=50, gender="male", height=1.7, weight=70, doctor_id="another_doctor").create()

    response = client.get("/patients/view")
    assert response.status_code == 200
    data = response.json()
    # Should only return patients for the logged-in doctor
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"


@pytest.mark.asyncio
async def test_view_patient_found(client):
    await Patient(id="P001", name="Alice", city="A", age=30, gender="female", height=1.6, weight=60, doctor_id="test_doctor").create()
    
    response = client.get("/patients/patient/P001")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


@pytest.mark.asyncio
async def test_view_patient_not_found(client):
    response = client.get("/patients/patient/P001")
    assert response.status_code == 404
    assert response.json() == {"detail": "Patient not found"}


@pytest.mark.asyncio
async def test_view_patient_wrong_doctor(client):
    await Patient(id="P001", name="Alice", city="A", age=30, gender="female", height=1.6, weight=60, doctor_id="another_doctor").create()
    
    response = client.get("/patients/patient/P001")
    assert response.status_code == 404
    assert response.json() == {"detail": "Patient not found"}


@pytest.mark.asyncio
async def test_create_patient_success(client):
    patient_data = {"id": "P003", "name": "Charlie", "city": "New City", "age": 45, "gender": "male", "height": 1.8, "weight": 80}
    response = client.post("/patients/create", json=patient_data)
    
    assert response.status_code == 201
    assert response.json() == {'message': 'patient created successfully'}
    
    # Verify it was created correctly in the mock database
    patient = await Patient.get("P003")
    assert patient is not None
    assert patient.name == "Charlie"
    assert patient.doctor_id == "test_doctor"


@pytest.mark.asyncio
async def test_create_patient_already_exists(client):
    await Patient(id="P001", name="Alice", city="A", age=30, gender="female", height=1.6, weight=60, doctor_id="test_doctor").create()
    
    patient_data = {"id": "P001", "name": "Alice", "city": "Testville", "age": 30, "gender": "female", "height": 1.6, "weight": 60}
    response = client.post("/patients/create", json=patient_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Patient already exists"}


@pytest.mark.asyncio
async def test_update_patient_success(client):
    await Patient(id="P001", name="Alice", city="Old City", age=30, gender="female", height=1.6, weight=60, doctor_id="test_doctor").create()
    
    response = client.put("/patients/edit/P001", json={"city": "New City"})
    assert response.status_code == 200
    assert response.json() == {'message': 'patient updated'}
    
    # Verify the change in the mock database
    updated_patient = await Patient.get("P001")
    assert updated_patient.city == "New City"


@pytest.mark.asyncio
async def test_delete_patient_success(client):
    await Patient(id="P001", name="Alice", city="Testville", age=30, gender="female", height=1.6, weight=60, doctor_id="test_doctor").create()
    
    response = client.delete("/patients/delete/P001")
    assert response.status_code == 200
    assert response.json() == {'message': 'patient deleted'}
    
    # Verify it's gone from the mock database
    deleted_patient = await Patient.get("P001")
    assert deleted_patient is None
