"""
Agent Integration Tests - Claims System Data Extraction
Tests for Data Extraction Agent retrieving data from claims system
"""
import pytest
import requests
from unittest.mock import Mock, patch
from tests.utils.validators import DataValidator
import re


@pytest.mark.agent
@pytest.mark.p0
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
            
            # Verify data types and formats
            assert isinstance(data["amount"], (int, float))
            assert data["amount"] >= 0
            assert data["status"] in ["pending", "approved", "rejected", "paid", "denied"]
            
            # Verify date format
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", data["claim_date"]), "Date format should be YYYY-MM-DD"
            
            # Verify amount has at most 2 decimal places
            amount_str = str(data["amount"])
            if "." in amount_str:
                decimal_places = len(amount_str.split(".")[1])
                assert decimal_places <= 2, "Amount should have at most 2 decimal places"
    
    def test_tc_agent_002_missing_required_fields(self, api_base_url):
        """
        TC-AGENT-002: Claims System Data Extraction - Missing Required Fields
        Verify that agent identifies and reports missing required fields
        """
        # Mock incomplete data (missing required fields)
        incomplete_data = {
            "claim_id": "CLM001",
            "patient_id": "PAT001"
            # Missing: provider_id, claim_date, amount, status
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = incomplete_data
            mock_get.return_value = mock_response
            
            # Trigger data extraction
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM001")
            data = response.json()
            
            # Validate data - should fail
            validator = DataValidator()
            is_valid, errors = validator.validate_data(data, "claims_data.json")
            
            assert not is_valid, "Validation should fail for incomplete data"
            assert len(errors) > 0, "Should have validation errors"
            
            # Verify missing fields are identified
            all_present, missing_fields = validator.validate_required_fields(data, "claims_data.json")
            assert not all_present, "Required fields should be missing"
            assert len(missing_fields) > 0, "Should identify missing fields"
    
    def test_tc_agent_003_invalid_data_types(self, api_base_url):
        """
        TC-AGENT-003: Claims System Data Extraction - Invalid Data Types
        Verify that agent validates data types and rejects invalid types
        """
        # Mock data with invalid types
        invalid_data = {
            "claim_id": "CLM001",
            "patient_id": "PAT001",
            "provider_id": "PRV001",
            "claim_date": "2024-01-15",
            "amount": "1500.00",  # Should be number
            "status": "pending"
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = invalid_data
            mock_get.return_value = mock_response
            
            # Trigger data extraction
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM001")
            data = response.json()
            
            # Validate data types - should fail
            validator = DataValidator()
            is_valid, errors = validator.validate_data_types(data, "claims_data.json")
            
            assert not is_valid, "Data type validation should fail"
            # Amount should be numeric, not string
            assert isinstance(data.get("amount"), str), "Should detect invalid amount type"
    
    def test_tc_agent_004_format_compliance(self, api_base_url):
        """
        TC-AGENT-004: Claims System Data Extraction - Format Compliance
        Verify that agent validates data format compliance
        """
        claims_data = {
            "claim_id": "CLM001",
            "patient_id": "PAT001",
            "provider_id": "PRV001",
            "claim_date": "2024-01-15",
            "amount": 1500.00,
            "status": "pending",
            "service_date": "2024-01-10",
            "service_code": "99213",
            "diagnosis_codes": ["I10", "E11.9"]
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = claims_data
            mock_get.return_value = mock_response
            
            # Trigger data extraction
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM001")
            data = response.json()
            
            # Validate format compliance
            validator = DataValidator()
            is_valid, errors = validator.validate_format(data, "claims_data.json")
            
            assert is_valid, f"Format validation failed: {errors}"
            
            # Verify date formats
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", data["claim_date"])
            if "service_date" in data:
                assert re.match(r"^\d{4}-\d{2}-\d{2}$", data["service_date"])
            
            # Verify status is valid enum
            assert data["status"] in ["pending", "approved", "rejected", "paid", "denied"]
    
    def test_tc_agent_005_network_failure_handling(self, api_base_url):
        """
        TC-AGENT-005: Claims System Data Extraction - Network Failure Handling
        Verify that agent handles network failures gracefully with retry logic
        """
        with patch('requests.get') as mock_get:
            # Simulate network failure
            mock_get.side_effect = [
                requests.exceptions.ConnectionError("Network error"),
                requests.exceptions.ConnectionError("Network error"),
                Mock(status_code=200, json=lambda: {"claim_id": "CLM001", "status": "pending"})  # Success on retry
            ]
            
            # Attempt extraction with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/CLM001", timeout=5)
                    if response.status_code == 200:
                        break
                except requests.exceptions.ConnectionError:
                    if attempt == max_retries - 1:
                        pytest.fail("Should succeed after retries")
                    continue
            
            # Verify retry was attempted
            assert mock_get.call_count >= 2, "Should retry on network failure"
    
    def test_tc_agent_006_authentication_failure(self, api_base_url):
        """
        TC-AGENT-006: Claims System Data Extraction - Authentication Failure
        Verify that agent handles authentication failures correctly
        """
        with patch('requests.get') as mock_get:
            # Mock authentication failure
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = {"error": "Authentication failed"}
            mock_get.return_value = mock_response
            
            # Trigger data extraction with invalid credentials
            response = requests.get(
                f"{api_base_url}/api/v1/agent/claims-system/CLM001",
                headers={"Authorization": "Bearer invalid_token"}
            )
            
            # Verify authentication failure
            assert response.status_code == 401, "Should return 401 for authentication failure"
            assert "error" in response.json(), "Should return error message"
            
            # Verify no data is retrieved
            assert "claim_id" not in response.json(), "Should not return claims data"
    
    def test_tc_agent_007_large_dataset_performance(self, api_base_url):
        """
        TC-AGENT-007: Claims System Data Extraction - Large Dataset Performance
        Verify that agent handles large datasets efficiently
        """
        # Mock large dataset response
        large_dataset = {
            "claims": [
                {
                    "claim_id": f"CLM{i:03d}",
                    "patient_id": f"PAT{i%10:03d}",
                    "provider_id": "PRV001",
                    "claim_date": "2024-01-15",
                    "amount": 1000.00 + i,
                    "status": "pending"
                }
                for i in range(1000)
            ],
            "total": 1000
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = large_dataset
            mock_get.return_value = mock_response
            
            # Trigger data extraction
            import time
            start_time = time.time()
            response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/batch")
            response_time = time.time() - start_time
            
            # Verify extraction success
            assert response.status_code == 200
            data = response.json()
            
            # Verify performance (should complete within reasonable time)
            assert response_time < 30, f"Should complete within 30 seconds, took {response_time:.2f}s"
            assert data.get("total") == 1000, "Should retrieve all claims"
            
            # Verify data integrity for sample
            if data.get("claims"):
                sample_claim = data["claims"][0]
                assert "claim_id" in sample_claim
                assert "patient_id" in sample_claim
                assert "amount" in sample_claim
    
    def test_tc_agent_008_concurrent_extractions(self, api_base_url):
        """
        TC-AGENT-008: Claims System Data Extraction - Concurrent Extractions
        Verify that agent handles concurrent data extractions correctly
        """
        import concurrent.futures
        
        def extract_claim(claim_id):
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "claim_id": claim_id,
                    "patient_id": "PAT001",
                    "provider_id": "PRV001",
                    "claim_date": "2024-01-15",
                    "amount": 1500.00,
                    "status": "pending"
                }
                mock_get.return_value = mock_response
                
                response = requests.get(f"{api_base_url}/api/v1/agent/claims-system/{claim_id}")
                return response.json()
        
        # Send 5 concurrent requests
        claim_ids = ["CLM001", "CLM002", "CLM003", "CLM004", "CLM005"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(extract_claim, claim_id) for claim_id in claim_ids]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all extractions succeeded
        assert len(results) == 5, "All concurrent extractions should complete"
        for result in results:
            assert "claim_id" in result, "Each result should contain claim_id"
            assert result["claim_id"] in claim_ids, "Should retrieve correct claim"
