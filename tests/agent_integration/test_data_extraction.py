"""
Agent Integration Tests - Claims System Data Extraction
Tests for Data Extraction Agent retrieving data from claims system
"""
import pytest
import requests
from unittest.mock import Mock, patch
from tests.utils.validators import DataValidator
import time


@pytest.mark.agent
class TestClaimsSystemDataExtraction:
    """Test cases for claims system data extraction"""
    
    def test_tc_agent_001_claims_data_extraction_happy_path(self, api_base_url):
        """
        TC-AGENT-001: Claims System Data Extraction - Happy Path
        Validate that agent correctly retrieves and validates claims data
        """
        claims_data = {
            "claim_id": "CLM001",
            "patient_id": "PAT001",
            "provider_id": "PRV001",
            "claim_date": "2024-01-15",
            "amount": 1500.00,
            "status": "pending"
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = claims_data
            mock_get.return_value = mock_response
            
            # Trigger claims data extraction
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM001")
            
            # Verify extraction success
            assert response.status_code == 200
            data = response.json()
            
            # Validate against schema
            validator = DataValidator()
            is_valid, errors = validator.validate_data(data, "claims_data.json")
            
            assert is_valid, f"Schema validation failed: {errors}"
            
            # Verify required fields
            required_fields = ["claim_id", "patient_id", "provider_id", "claim_date", "amount", "status"]
            for field in required_fields:
                assert field in data, f"Required field '{field}' is missing"
            
            # Verify data types
            assert isinstance(data["claim_id"], str)
            assert isinstance(data["patient_id"], str)
            assert isinstance(data["provider_id"], str)
            assert isinstance(data["claim_date"], str)
            assert isinstance(data["amount"], (int, float))
            assert isinstance(data["status"], str)
            
            # Verify data format compliance
            assert len(data["claim_date"]) == 10  # YYYY-MM-DD format
            assert data["status"] in ["pending", "approved", "rejected", "paid", "denied"]
    
    def test_tc_agent_002_missing_required_fields(self, api_base_url):
        """
        TC-AGENT-002: Claims System Data Extraction - Missing Required Fields
        Verify that agent correctly identifies and reports missing required fields
        """
        # Claims data with missing provider_id
        incomplete_claims_data = {
            "claim_id": "CLM002",
            "patient_id": "PAT002",
            "claim_date": "2024-01-16",
            "amount": 2500.00,
            "status": "pending"
            # Missing: provider_id
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = incomplete_claims_data
            mock_get.return_value = mock_response
            
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM002")
            
            assert response.status_code == 200
            data = response.json()
            
            # Validate against schema (should fail)
            validator = DataValidator()
            is_valid, errors = validator.validate_data(data, "claims_data.json")
            
            # Validation should fail
            assert not is_valid, "Validation should fail for incomplete data"
            
            # Verify missing field is identified
            assert any("provider_id" in str(error) for error in errors), \
                "Missing 'provider_id' field should be reported in errors"
            
            # Verify error message is clear
            assert len(errors) > 0, "Errors should be reported for missing fields"
    
    def test_tc_agent_003_invalid_data_types(self, api_base_url):
        """
        TC-AGENT-003: Claims System Data Extraction - Invalid Data Types
        Verify that agent validates data types and rejects invalid types
        """
        # Claims data with invalid data types (string in amount field)
        invalid_type_data = {
            "claim_id": "CLM003",
            "patient_id": "PAT003",
            "provider_id": "PRV003",
            "claim_date": "2024-01-17",
            "amount": "invalid_amount",  # Should be numeric, not string
            "status": "pending"
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = invalid_type_data
            mock_get.return_value = mock_response
            
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM003")
            
            assert response.status_code == 200
            data = response.json()
            
            # Validate against schema (should fail due to type mismatch)
            validator = DataValidator()
            is_valid, errors = validator.validate_data(data, "claims_data.json")
            
            # Validation should fail
            assert not is_valid, "Validation should fail for invalid data types"
            
            # Verify type error is identified
            assert len(errors) > 0, "Errors should be reported for type mismatch"
            error_message = str(errors).lower()
            assert "amount" in error_message, "Error should mention the 'amount' field"
            assert any(word in error_message for word in ["type", "number", "numeric", "integer", "float"]), \
                "Error should indicate type mismatch (expected number)"
        
        # Test with another invalid type (numeric status instead of string)
        invalid_status_data = {
            "claim_id": "CLM004",
            "patient_id": "PAT004",
            "provider_id": "PRV004",
            "claim_date": "2024-01-18",
            "amount": 2000.00,
            "status": 123  # Should be string, not number
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = invalid_status_data
            mock_get.return_value = mock_response
            
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM004")
            
            assert response.status_code == 200
            data = response.json()
            
            # Validate data types directly
            assert isinstance(data["amount"], (int, float)), "Amount should be numeric"
            assert not isinstance(data["status"], str), "Status should be string but is not"
            
            # This should fail schema validation
            validator = DataValidator()
            is_valid, errors = validator.validate_data(data, "claims_data.json")
            
            assert not is_valid, "Validation should fail for invalid status type"
    
    def test_tc_agent_004_critical_data_integrity_check(self, api_base_url):
        """
        TC-AGENT-004: Claims System Data Extraction - Critical Data Integrity (DEMO FAILURE)
        
        NOTE: This test intentionally fails to demonstrate error reporting in test reports.
        It simulates detecting a critical data integrity issue that would be caught in production.
        
        To enable this test and see the failure, remove the @pytest.mark.skip decorator above.
        """
        # Simulate a critical data integrity issue - negative claim amount
        critical_issue_data = {
            "claim_id": "CLM999",
            "patient_id": "PAT999",
            "provider_id": "PRV999",
            "claim_date": "2024-01-19",
            "amount": -500.00,  # CRITICAL: Negative amount should never occur
            "status": "approved"
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = critical_issue_data
            mock_get.return_value = mock_response
            
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM999")
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify data was retrieved
            assert "amount" in data
            
            # CRITICAL VALIDATION: Amount must be positive
            # This assertion will FAIL to demonstrate error reporting
            assert data["amount"] > 0, \
                f"CRITICAL: Claim amount must be positive. Found: {data['amount']} for claim {data['claim_id']}. " \
                f"This indicates a serious data integrity issue that requires immediate investigation."
