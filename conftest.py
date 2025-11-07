"""
Global pytest configuration and shared fixtures
"""
import os
import pytest
import yaml
from pathlib import Path
from dotenv import load_dotenv
from unittest.mock import Mock, MagicMock
import json

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent / "config" / ".env")

# Load test configuration
CONFIG_PATH = Path(__file__).parent / "config" / "test_config.yaml"
with open(CONFIG_PATH, 'r') as f:
    TEST_CONFIG = yaml.safe_load(f)


@pytest.fixture(scope="session")
def config():
    """Load test configuration"""
    return TEST_CONFIG


@pytest.fixture(scope="session")
def api_base_url():
    """API base URL from environment"""
    return os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def test_data_path():
    """Path to test data fixtures"""
    return Path(__file__).parent / "fixtures" / "data"


@pytest.fixture(scope="session")
def schemas_path():
    """Path to JSON schemas"""
    return Path(__file__).parent / "fixtures" / "schemas"


@pytest.fixture
def patient_record_schema(schemas_path):
    """Load patient record schema"""
    schema_path = schemas_path / "patient_record.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def medical_chart_schema(schemas_path):
    """Load medical chart schema"""
    schema_path = schemas_path / "medical_chart.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def claims_data_schema(schemas_path):
    """Load claims data schema"""
    schema_path = schemas_path / "claims_data.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def mock_patient_portal():
    """Mock patient portal API"""
    mock = MagicMock()
    mock.get_patient_data.return_value = {
        "patient_id": "PAT001",
        "name": "John Doe",
        "dob": "1980-01-15",
        "ssn": "***-**-1234",
        "medical_record_number": "MRN123456"
    }
    return mock


@pytest.fixture
def mock_fax_system():
    """Mock fax system API"""
    mock = MagicMock()
    mock.receive_fax.return_value = {
        "fax_id": "FAX001",
        "received_at": "2024-01-15T10:30:00Z",
        "pages": 5,
        "format": "pdf",
        "content": b"Mock PDF content"
    }
    return mock


@pytest.fixture
def mock_claims_system():
    """Mock claims system API"""
    mock = MagicMock()
    mock.get_claim.return_value = {
        "claim_id": "CLM001",
        "patient_id": "PAT001",
        "provider_id": "PRV001",
        "claim_date": "2024-01-15",
        "amount": 1500.00,
        "status": "pending"
    }
    return mock


@pytest.fixture
def sample_patient_data():
    """Sample patient data for testing"""
    return {
        "patient_id": "PAT001",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1980-01-15",
        "gender": "M",
        "ssn": "123-45-6789",
        "address": {
            "street": "123 Main St",
            "city": "Boston",
            "state": "MA",
            "zip": "02101"
        },
        "phone": "617-555-1234",
        "email": "john.doe@example.com",
        "medical_record_number": "MRN123456",
        "insurance": {
            "provider": "Blue Cross",
            "policy_number": "POL123456",
            "group_number": "GRP789"
        }
    }


@pytest.fixture
def sample_medical_chart():
    """Sample medical chart data"""
    return {
        "chart_id": "CHT001",
        "patient_id": "PAT001",
        "visit_date": "2024-01-15",
        "provider": "Dr. Jane Smith",
        "chief_complaint": "Chest pain",
        "history_of_present_illness": "Patient reports chest pain for 2 hours",
        "vital_signs": {
            "blood_pressure": "120/80",
            "heart_rate": 72,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "assessment": "Chest pain, rule out cardiac",
        "plan": "EKG, chest X-ray, labs"
    }


@pytest.fixture
def sample_risk_classification_input():
    """Sample input for risk classification model"""
    return {
        "patient_id": "PAT001",
        "age": 44,
        "symptoms": ["chest_pain", "shortness_of_breath"],
        "vital_signs": {
            "blood_pressure": "140/90",
            "heart_rate": 95
        },
        "medical_history": ["hypertension", "diabetes"],
        "medications": ["lisinopril", "metformin"]
    }


@pytest.fixture
def sample_sentiment_analysis_input():
    """Sample input for sentiment analysis model"""
    return {
        "text": "I've been experiencing chest pain for the past few hours. I'm really worried about it.",
        "patient_id": "PAT001",
        "context": "patient_portal_message"
    }
