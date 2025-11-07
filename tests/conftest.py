"""
Pytest configuration and shared fixtures
"""
import os
import pytest


@pytest.fixture(scope="session")
def api_base_url():
    """API base URL from environment"""
    return os.getenv("API_BASE_URL", "http://localhost:8000")


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
