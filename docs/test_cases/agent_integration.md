# Agent Integration Test Cases

## Overview
Test cases for validating Data Extraction Agent's ability to retrieve and validate data from a claims system. Focuses on data extraction accuracy, data type validation, and format compliance.

---

## TC-AGENT-001: Claims Data Extraction - Happy Path
**Category**: Data Extraction Accuracy  
**Priority**: High | **Risk**: High | **Complexity**: Medium

### Objective
Validate that the Data Extraction Agent correctly retrieves claims data from the claims system and validates it against a predefined schema.

### Prerequisites
- Claims system is accessible
- Test claim (ID: CLM001) exists in system
- Agent is configured with valid credentials
- JSON schema for claims data is defined

### Test Steps
1. Configure Data Extraction Agent to connect to claims system
2. Trigger data extraction for claim ID: CLM001
3. Verify agent successfully connects and authenticates
4. Verify agent retrieves claims data
5. Validate retrieved data against claims data schema (`tests/fixtures/schemas/claims_data.json`)
6. Verify all required fields are present (claim_id, patient_id, provider_id, claim_date, amount, status)
7. Verify data types match schema (strings, dates, numbers)
8. Verify data format compliance (dates: YYYY-MM-DD, amounts: numeric with 2 decimals)

### Expected Results
- Agent successfully connects to claims system with authentication
- Claims data is retrieved without errors
- All required fields are present in response
- Data types match schema definition:
  - `claim_id`: string
  - `patient_id`: string
  - `provider_id`: string
  - `claim_date`: string (YYYY-MM-DD format)
  - `amount`: number (max 2 decimal places)
  - `status`: enum (pending, approved, rejected, paid, denied)
- Data validation passes with no schema violations
- Extraction completes within acceptable time (< 5 seconds)

### Pass/Fail Criteria
- **Pass**: All validations pass, data matches schema, no missing/invalid fields
- **Fail**: Any validation fails, missing required fields, incorrect data types, or format violations

### Test Data
```json
{
  "claim_id": "CLM001",
  "patient_id": "PAT001",
  "provider_id": "PRV001",
  "claim_date": "2024-01-15",
  "amount": 1500.00,
  "status": "pending"
}
```

---

## TC-AGENT-002: Claims Data Extraction - Missing Required Fields
**Category**: Data Validation  
**Priority**: Critical | **Risk**: Critical | **Complexity**: Low

### Objective
Verify that the agent correctly identifies and reports missing required fields in extracted data.

### Prerequisites
- Claims system configured with incomplete test claim (ID: CLM002)
- Agent is configured
- Schema validation is enabled

### Test Steps
1. Configure agent to extract claim CLM002 (missing `provider_id` field)
2. Trigger data extraction
3. Verify agent retrieves data
4. Run schema validation
5. Verify validation fails
6. Verify error message identifies missing field
7. Verify agent does not proceed with incomplete data
8. Verify error is logged appropriately

### Expected Results
- Agent retrieves incomplete data successfully
- Schema validation fails immediately
- Clear error message: "Validation failed: Required field 'provider_id' is missing"
- Error includes:
  - Field name that is missing
  - Claim ID being processed
  - Timestamp of validation
- Agent stops processing and does not save incomplete data
- Error is logged with appropriate severity level
- No partial data is committed to downstream systems

### Pass/Fail Criteria
- **Pass**: Missing fields detected, clear error message, processing stopped
- **Fail**: Missing fields not detected, unclear error, or incomplete data is processed

### Test Data
```json
{
  "claim_id": "CLM002",
  "patient_id": "PAT002",
  "claim_date": "2024-01-16",
  "amount": 2500.00,
  "status": "pending"
  // Missing: provider_id
}
```

---

## TC-AGENT-003: Claims Data Extraction - Network Failure Handling
**Category**: Error Handling & Resilience  
**Priority**: High | **Risk**: High | **Complexity**: High

### Objective
Verify that the agent handles network failures gracefully with appropriate retry logic and error reporting.

### Prerequisites
- Claims system is accessible initially
- Ability to simulate network failure (disconnect network or mock timeout)
- Agent retry configuration is set (3 attempts with exponential backoff)

### Test Steps
1. Configure agent to connect to claims system
2. Start data extraction for claim CLM003
3. Simulate network failure during extraction (disconnect or timeout)
4. Observe agent behavior
5. Verify retry attempts are made
6. Verify exponential backoff between retries
7. Restore network connection
8. Verify extraction completes successfully after network restore
9. Verify all retry attempts are logged

### Expected Results
- Network failure is detected immediately
- Agent implements retry logic:
  - Attempt 1: Immediate retry
  - Attempt 2: 2 second delay
  - Attempt 3: 4 second delay
- Each retry is logged with timestamp and attempt number
- Error messages are descriptive: "Network connection failed. Retrying... (Attempt 2/3)"
- After network restore, extraction succeeds
- Total retry time does not exceed configured timeout (30 seconds)
- Final status indicates successful recovery
- Data integrity is maintained (no partial/corrupted data)

### Pass/Fail Criteria
- **Pass**: Network failure handled, retry logic works, extraction succeeds after restore
- **Fail**: No retry attempts, immediate failure, or data corruption

### Test Data
- Same as TC-AGENT-001 (CLM001)
- Network simulation: 10-second outage during extraction

---

## Suggested Additional Test Scenarios

### TC-AGENT-004: Invalid Data Types Validation
Verify agent rejects data when field types don't match schema (e.g., string in amount field instead of number). Expected: Clear error message specifying field name, expected type vs actual type, and claim ID being processed.

### TC-AGENT-005: Authentication Failure Handling
Test agent behavior with invalid or expired credentials. Expected: Immediate authentication failure with clear error, no retry attempts with bad credentials, security event logged to audit trail.

---

## Test Environment Requirements
- **Claims System**: Mock or test environment with controllable test data
- **Network Control**: Ability to simulate failures, latency, timeouts
- **Monitoring**: Log access to verify error handling and retry behavior
- **Schema Files**: JSON schemas in `tests/fixtures/schemas/`

## Automation Notes
Automated tests use pytest with mocking:
- `@patch` decorators to mock API calls
- `Mock` objects to simulate responses and failures
- Schema validation using `jsonschema` library
- Network failures simulated via mock exceptions

See: `tests/agent_integration/test_data_extraction.py`
