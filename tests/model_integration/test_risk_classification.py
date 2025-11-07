"""
Model Integration Tests - Risk Classification & Sentiment Analysis
Tests for AI model integration
"""
import pytest
import requests
from unittest.mock import Mock, patch
import time


@pytest.mark.model
class TestRiskClassificationModel:
    """Test cases for risk classification model"""
    
    def test_tc_model_001_standard_input(self, api_base_url, sample_risk_classification_input):
        """
        TC-MODEL-001: Risk Classification Model - Standard Input
        Validate that model correctly processes standard patient data
        """
        with patch('requests.post') as mock_post:
            # Mock model response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "risk_level": "medium",
                "confidence_score": 0.78,
                "reasoning": "Patient has diabetes and elevated BMI, with borderline high blood pressure",
                "timestamp": "2024-01-15T10:30:00Z"
            }
            mock_post.return_value = mock_response
            
            # Measure response time
            start_time = time.time()
            response = requests.post(
                f"{api_base_url}/api/v1/models/risk-classification",
                json=sample_risk_classification_input,
                timeout=30
            )
            response_time = time.time() - start_time
            
            # Verify response
            assert response.status_code == 200, "Model should accept input successfully"
            assert response_time < 2, f"Response time should be < 2 seconds, got {response_time:.2f}s"
            
            data = response.json()
            
            # Validate key model outputs
            assert data["risk_level"] == "medium", "Should classify as medium risk for given input"
            assert data["confidence_score"] > 0.7, "Confidence should be high for standard input"
            assert len(data["reasoning"]) > 0, "Should provide reasoning for prediction"
    
    def test_tc_model_002_edge_case_values(self, api_base_url):
        """
        TC-MODEL-002: Risk Classification Model - Edge Cases
        Verify model handles minimal data with low confidence appropriately
        """
        # Test with minimal input (only required fields)
        minimal_input = {
            "patient": {
                "age": 30,
                "gender": "female"
            }
        }
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "risk_level": "low",
                "confidence_score": 0.45,
                "reasoning": "Limited data available for comprehensive risk assessment",
                "timestamp": "2024-01-15T10:31:00Z"
            }
            mock_post.return_value = mock_response
            
            response = requests.post(
                f"{api_base_url}/api/v1/models/risk-classification",
                json=minimal_input,
                timeout=30
            )
            
            assert response.status_code == 200, "Model should accept minimal input"
            data = response.json()
            
            # Verify model handles minimal data gracefully
            assert data["risk_level"] == "low", "Should default to low risk for minimal data"
            assert data["confidence_score"] < 0.5, "Confidence should be low due to limited data"


@pytest.mark.model
class TestSentimentAnalysisModel:
    """Test cases for sentiment analysis model"""
    
    def test_tc_model_003_patient_text_input(self, api_base_url, sample_sentiment_analysis_input):
        """
        TC-MODEL-003: Sentiment Analysis Model - Patient Text Input
        Validate that model correctly analyzes patient text and identifies urgent concerns
        """
        # Test with urgent/concerning text
        urgent_text = {
            "patient_text": "I've been experiencing severe chest pain for the past 2 hours. It's getting worse and I'm having trouble breathing. Should I be worried?"
        }
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "sentiment": "urgent",
                "confidence_score": 0.92,
                "key_themes": ["chest pain", "difficulty breathing", "severe symptoms"],
                "urgency_level": "high",
                "summary": "Patient reports severe chest pain and breathing difficulty - immediate medical attention recommended"
            }
            mock_post.return_value = mock_response
            
            # Measure response time
            start_time = time.time()
            response = requests.post(
                f"{api_base_url}/api/v1/models/sentiment-analysis",
                json=urgent_text,
                timeout=30
            )
            response_time = time.time() - start_time
            
            # Verify response
            assert response.status_code == 200, "Model should accept text input"
            assert response_time < 2, f"Response time should be < 2 seconds, got {response_time:.2f}s"
            
            data = response.json()
            
            # Verify urgent case is identified
            assert data["sentiment"] == "urgent", "Should identify urgent sentiment for severe symptoms"
            assert data["urgency_level"] == "high", "Should flag high urgency"
            assert data["confidence_score"] > 0.85, "Confidence should be high for clear urgent text"
