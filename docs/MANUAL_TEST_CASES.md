# Manual Test Cases

## Overview

This document outlines manual test cases for the Autonomize AI platform, clearly distinguishing between automated and manual test procedures. Automated tests are executed via pytest and are documented in the test code, while manual tests require human verification and interaction.

---

## Test Case Classification

- **🔵 Automated**: Executed automatically via pytest test suite
- **🟡 Manual**: Requires human verification and manual execution
- **🟢 Hybrid**: Partially automated with manual verification steps

---

## 1. Agent Integration Test Cases

### TC-AGENT-001: Claims Data Extraction - Happy Path
**Status**: 🔵 **Automated**  
**Test File**: `tests/agent_integration/test_data_extraction.py::test_tc_agent_001_claims_data_extraction_happy_path`

**Automated Test Coverage**:
- ✅ API connection and authentication
- ✅ Data retrieval from claims system
- ✅ Schema validation (required fields, data types, formats)
- ✅ Response time measurement

**Manual Verification Steps** (if needed):
1. Verify actual claims system is accessible
2. Verify test claim ID exists in system
3. Manually inspect retrieved data in external system
4. Verify data matches expected values

**Execution**:
```bash
uv run pytest tests/agent_integration/test_data_extraction.py::test_tc_agent_001_claims_data_extraction_happy_path -v
```

---

### TC-AGENT-002: Missing Required Fields Validation
**Status**: 🔵 **Automated**  
**Test File**: `tests/agent_integration/test_data_extraction.py::test_tc_agent_002_missing_required_fields`

**Automated Test Coverage**:
- ✅ Detection of missing required fields
- ✅ Schema validation failure reporting
- ✅ Error message clarity and specificity

**Manual Verification Steps** (if needed):
1. Verify error messages are user-friendly
2. Verify error logging includes appropriate context
3. Verify no partial data is saved when validation fails

**Execution**:
```bash
uv run pytest tests/agent_integration/test_data_extraction.py::test_tc_agent_002_missing_required_fields -v
```

---

### TC-AGENT-003: Invalid Data Types Handling
**Status**: 🔵 **Automated**  
**Test File**: `tests/agent_integration/test_data_extraction.py::test_tc_agent_003_invalid_data_types`

**Automated Test Coverage**:
- ✅ Type mismatch detection (string vs number, etc.)
- ✅ Error reporting for type violations
- ✅ Multiple type error scenarios

**Manual Verification Steps** (if needed):
1. Verify error messages clearly indicate expected vs actual types
2. Verify error messages include field names and claim IDs

**Execution**:
```bash
uv run pytest tests/agent_integration/test_data_extraction.py::test_tc_agent_003_invalid_data_types -v
```

---

### TC-AGENT-004: Critical Data Integrity Check
**Status**: 🔵 **Automated** (Skipped by default for demo purposes)  
**Test File**: `tests/agent_integration/test_data_extraction.py::test_tc_agent_004_critical_data_integrity_check`

**Automated Test Coverage**:
- ✅ Detection of critical data integrity issues (e.g., negative claim amounts)
- ✅ Error reporting for critical violations

**Manual Verification Steps**:
1. Remove `@pytest.mark.skip` decorator to enable test
2. Verify test failure demonstrates proper error reporting
3. Verify error messages indicate severity of issue

**Execution**:
```bash
# First, remove @pytest.mark.skip from test file, then:
uv run pytest tests/agent_integration/test_data_extraction.py::test_tc_agent_004_critical_data_integrity_check -v
```

---

### TC-AGENT-005: Network Failure Handling
**Status**: 🟡 **Manual**

**Objective**: Verify agent handles network failures gracefully with retry logic

**Prerequisites**:
- Agent configured and running
- Claims system accessible
- Ability to simulate network failure (disconnect network, firewall rules, etc.)

**Manual Test Steps**:
1. Start data extraction for a valid claim ID (e.g., CLM001)
2. While extraction is in progress, simulate network failure:
   - Option A: Disconnect network cable/disable WiFi
   - Option B: Block network traffic using firewall rules
   - Option C: Stop/restart claims system service
3. Observe agent behavior:
   - Verify retry attempts are logged
   - Verify exponential backoff timing (2s, 4s delays)
   - Verify error messages are clear
4. Restore network connectivity
5. Verify extraction completes successfully after network restore
6. Verify no data corruption occurred
7. Check logs for retry attempt details

**Expected Results**:
- Network failure detected within 5 seconds
- Retry attempts logged with timestamps
- Exponential backoff implemented (2s, 4s delays)
- Extraction succeeds after network restore
- No partial/corrupted data saved
- Total retry time < 30 seconds

**Pass/Fail Criteria**:
- **Pass**: Network failure handled gracefully, retries work, extraction succeeds after restore
- **Fail**: No retries, immediate failure, data corruption, or timeout exceeded

**Test Data**:
- Claim ID: CLM001
- Network outage duration: 10 seconds

---

### TC-AGENT-006: Authentication Failure Handling
**Status**: 🟡 **Manual**

**Objective**: Verify agent handles authentication failures appropriately

**Prerequisites**:
- Agent configured
- Ability to modify credentials or simulate auth failure

**Manual Test Steps**:
1. Configure agent with invalid credentials
2. Attempt data extraction for claim CLM001
3. Observe error handling:
   - Verify immediate failure (no retries with bad credentials)
   - Verify clear error message indicating authentication failure
   - Verify security event logged
4. Configure agent with expired token/credentials
5. Attempt data extraction
6. Verify appropriate error handling

**Expected Results**:
- Immediate authentication failure (no retries)
- Clear error message: "Authentication failed: Invalid credentials"
- Security event logged to audit trail
- No sensitive credential information in error messages

**Pass/Fail Criteria**:
- **Pass**: Immediate failure, clear error, security logged, no credential exposure
- **Fail**: Retries with bad credentials, unclear errors, or credential leakage

---

### TC-AGENT-007: Large Dataset Extraction
**Status**: 🟡 **Manual**

**Objective**: Verify agent handles large claims datasets efficiently

**Prerequisites**:
- Claims system with large dataset (1000+ claims)
- Performance monitoring tools

**Manual Test Steps**:
1. Extract data for single claim, measure time
2. Extract data for 10 claims sequentially, measure total time
3. Extract data for 100 claims sequentially, measure total time
4. Monitor:
   - Memory usage
   - CPU usage
   - Network bandwidth
   - Response times
5. Verify no memory leaks or performance degradation

**Expected Results**:
- Single claim extraction: < 5 seconds
- 10 claims: < 50 seconds (linear scaling)
- 100 claims: < 500 seconds
- Memory usage remains stable
- No timeout errors

**Pass/Fail Criteria**:
- **Pass**: Linear scaling, stable memory, no timeouts
- **Fail**: Exponential slowdown, memory leaks, or timeouts

---

## 2. Model Integration Test Cases

### TC-MODEL-001: Risk Classification Model - Standard Input
**Status**: 🔵 **Automated**  
**Test File**: `tests/model_integration/test_risk_classification.py::test_tc_model_001_standard_input`

**Automated Test Coverage**:
- ✅ Model accepts standard patient data
- ✅ Response time < 2 seconds
- ✅ Risk level classification accuracy
- ✅ Confidence score validation
- ✅ Reasoning field presence

**Manual Verification Steps** (if needed):
1. Verify reasoning text is clinically meaningful
2. Verify risk level matches clinical expectations for test case
3. Verify confidence score is reasonable

**Execution**:
```bash
uv run pytest tests/model_integration/test_risk_classification.py::test_tc_model_001_standard_input -v
```

---

### TC-MODEL-002: Risk Classification Model - Edge Cases
**Status**: 🔵 **Automated**  
**Test File**: `tests/model_integration/test_risk_classification.py::test_tc_model_002_edge_case_values`

**Automated Test Coverage**:
- ✅ Minimal input handling (age and gender only)
- ✅ Low confidence scores for limited data
- ✅ Appropriate default risk levels

**Manual Verification Steps** (if needed):
1. Verify reasoning indicates "limited data available"
2. Verify risk level is conservative (low) for minimal data
3. Test with boundary age values manually (0, 18, 65, 100)

**Execution**:
```bash
uv run pytest tests/model_integration/test_risk_classification.py::test_tc_model_002_edge_case_values -v
```

---

### TC-MODEL-003: Sentiment Analysis Model - Patient Text Input
**Status**: 🔵 **Automated**  
**Test File**: `tests/model_integration/test_risk_classification.py::test_tc_model_003_patient_text_input`

**Automated Test Coverage**:
- ✅ Sentiment classification (urgent, positive, negative, neutral)
- ✅ Urgency level assessment
- ✅ Key themes extraction
- ✅ Confidence score validation
- ✅ Response time < 2 seconds

**Manual Verification Steps** (if needed):
1. Verify extracted themes are accurate
2. Verify urgency level matches text content
3. Verify summary is clinically relevant

**Execution**:
```bash
uv run pytest tests/model_integration/test_risk_classification.py::test_tc_model_003_patient_text_input -v
```

---

### TC-MODEL-004: Model Response Consistency
**Status**: 🟡 **Manual**

**Objective**: Verify model produces consistent results for identical inputs

**Prerequisites**:
- Model endpoint accessible
- Test patient data prepared

**Manual Test Steps**:
1. Send same patient data to risk classification model 10 times
2. Record risk_level, confidence_score, and reasoning for each response
3. Compare results:
   - Verify risk_level is identical across all 10 calls
   - Verify confidence_score variance < 0.01
   - Verify reasoning is consistent (may have minor wording differences)
4. Repeat with sentiment analysis model using same text input

**Expected Results**:
- Risk level: 100% consistent across all calls
- Confidence score: Variance < 0.01
- Reasoning: Consistent meaning (minor wording differences acceptable)

**Pass/Fail Criteria**:
- **Pass**: Consistent risk levels, low confidence variance, consistent reasoning
- **Fail**: Inconsistent risk levels or high confidence variance

**Test Data**:
```json
{
  "patient": {
    "age": 45,
    "gender": "male",
    "medical_history": ["diabetes", "hypertension"],
    "vitals": {
      "blood_pressure": "140/90",
      "heart_rate": 82,
      "bmi": 28
    }
  }
}
```

---

### TC-MODEL-005: Model Performance Under Load
**Status**: 🟡 **Manual**

**Objective**: Verify model maintains performance under concurrent load

**Prerequisites**:
- Load testing tool (e.g., Apache Bench, JMeter, Locust)
- Model endpoint accessible
- Test data prepared

**Manual Test Steps**:
1. Measure baseline: Single request response time
2. Send 10 concurrent requests, measure:
   - Response times (min, max, average, 95th percentile)
   - Success rate
   - Error rate
3. Send 50 concurrent requests, repeat measurements
4. Send 100 concurrent requests, repeat measurements
5. Monitor server resources (CPU, memory, network)

**Expected Results**:
- Baseline: < 2 seconds
- 10 concurrent: 95th percentile < 3 seconds, 100% success
- 50 concurrent: 95th percentile < 5 seconds, > 95% success
- 100 concurrent: 95th percentile < 10 seconds, > 90% success
- No server crashes or memory leaks

**Pass/Fail Criteria**:
- **Pass**: Performance degrades gracefully, high success rate, no crashes
- **Fail**: Significant slowdown, high error rate, or crashes

**Tools**:
```bash
# Example using Apache Bench
ab -n 100 -c 10 -p test_data.json -T application/json http://localhost:8000/api/v1/models/risk-classification
```

---

### TC-MODEL-006: Model Input Validation
**Status**: 🟡 **Manual**

**Objective**: Verify model rejects invalid inputs with appropriate error messages

**Prerequisites**:
- Model endpoint accessible
- Invalid test data prepared

**Manual Test Steps**:
1. Send request with malformed JSON
2. Verify HTTP 400 error with clear message
3. Send request with missing required fields
4. Verify HTTP 400 error identifying missing fields
5. Send request with wrong data types (string instead of number)
6. Verify HTTP 400 error indicating type mismatch
7. Send request with invalid enum values
8. Verify HTTP 400 error indicating invalid enum value
9. Verify no 500 errors (server crashes)

**Expected Results**:
- Malformed JSON: HTTP 400, "Invalid JSON format"
- Missing fields: HTTP 400, "Missing required field: {field_name}"
- Type mismatch: HTTP 400, "Invalid type for field {field_name}: expected {type}, got {type}"
- Invalid enum: HTTP 400, "Invalid value for {field_name}: must be one of {valid_values}"
- No 500 errors for any invalid input

**Pass/Fail Criteria**:
- **Pass**: All invalid inputs rejected with clear errors, no 500 errors
- **Fail**: Unclear errors, 500 errors, or invalid inputs accepted

**Test Cases**:
```json
// Malformed JSON
{"patient": {age: 45}}

// Missing required field
{"patient": {"gender": "male"}}

// Wrong type
{"patient": {"age": "forty-five"}}

// Invalid enum
{"patient": {"gender": "unknown"}}
```

---

## 3. End-to-End Integration Test Cases

### TC-E2E-001: Complete Workflow - Claims to Risk Assessment
**Status**: 🟡 **Manual**

**Objective**: Verify complete workflow from claims extraction to risk assessment

**Prerequisites**:
- Agent and models configured and running
- Test claim exists in claims system

**Manual Test Steps**:
1. Extract claims data for claim CLM001 using agent
2. Verify data extraction succeeds and data is validated
3. Extract patient data from claims data (patient_id)
4. Retrieve patient medical history and vitals
5. Send patient data to risk classification model
6. Verify risk assessment is generated
7. Verify risk level is appropriate for patient data
8. If patient text available, send to sentiment analysis model
9. Verify sentiment analysis completes
10. Verify combined results are coherent

**Expected Results**:
- Data extraction succeeds
- Patient data retrieved successfully
- Risk classification generated with appropriate risk level
- Sentiment analysis (if applicable) completes successfully
- Results are clinically coherent

**Pass/Fail Criteria**:
- **Pass**: Complete workflow executes successfully, results are coherent
- **Fail**: Any step fails or results are inconsistent

---

## 4. UI/UX Test Cases

### TC-UI-001: Error Message Clarity
**Status**: 🟡 **Manual**

**Objective**: Verify error messages are clear and actionable for users

**Manual Test Steps**:
1. Trigger various error scenarios:
   - Missing required fields
   - Invalid data types
   - Network failures
   - Authentication failures
2. Review error messages displayed to users
3. Verify messages:
   - Are written in plain language (not technical jargon)
   - Indicate what went wrong
   - Suggest how to fix the issue
   - Include relevant context (claim ID, field name, etc.)

**Expected Results**:
- Error messages are clear and non-technical
- Messages indicate specific problem
- Messages suggest remediation steps
- Context included (IDs, field names)

**Pass/Fail Criteria**:
- **Pass**: Messages are clear, actionable, and include context
- **Fail**: Messages are unclear, technical, or lack context

---

## Summary

### Automated Tests (🔵)
- **Agent Integration**: 4 automated tests
- **Model Integration**: 3 automated tests
- **Total Automated**: 7 tests

### Manual Tests (🟡)
- **Agent Integration**: 3 manual tests
- **Model Integration**: 3 manual tests
- **End-to-End**: 1 manual test
- **UI/UX**: 1 manual test
- **Total Manual**: 8 tests

### Running All Automated Tests
```bash
# Run all automated tests
uv run pytest tests/ -v

# Run with HTML report
uv run pytest tests/ -v --html=reports/report.html --self-contained-html

# Run specific test suites
uv run pytest tests/agent_integration/ -v -m agent
uv run pytest tests/model_integration/ -v -m model
```

---

## Document Version

- **Version**: 1.0
- **Last Updated**: 2024-01-15

