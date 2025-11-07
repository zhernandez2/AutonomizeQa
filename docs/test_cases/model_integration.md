# Model Integration Test Cases

## Overview
Test cases for validating AI model integration, focusing on risk classification and sentiment analysis models. Tests validate model input/output handling, data format variations, and response accuracy.

---

## TC-MODEL-001: Risk Classification Model - Standard Input
**Category**: Model Accuracy  
**Priority**: High | **Risk**: High | **Complexity**: Medium

### Objective
Validate that the risk classification model correctly processes standard patient data and returns accurate risk predictions with appropriate confidence scores.

### Prerequisites
- Risk classification model endpoint is accessible
- Model is trained and deployed
- Test patient data is available
- Expected risk categories are defined (low, medium, high, critical)

### Test Steps
1. Prepare standard patient input data (age, medical history, vitals)
2. Send POST request to risk classification endpoint
3. Verify request is accepted (HTTP 200)
4. Verify response contains required fields
5. Verify risk_level is valid enum value
6. Verify confidence_score is numeric and in range [0-1]
7. Verify reasoning field provides explanation
8. Compare prediction against expected outcome for known case

### Expected Results
- HTTP 200 status code returned
- Response time < 2 seconds
- Response contains all required fields:
  - `risk_level`: enum (low, medium, high, critical)
  - `confidence_score`: float between 0.0 and 1.0
  - `reasoning`: string explaining the prediction
  - `timestamp`: ISO 8601 format
- For test input (45-year-old with diabetes, BMI 28):
  - Expected `risk_level`: "medium"
  - Confidence score > 0.7
  - Reasoning mentions diabetes and BMI
- Response is consistent on repeated calls with same input

### Pass/Fail Criteria
- **Pass**: All required fields present, valid values, correct prediction for known case
- **Fail**: Missing fields, invalid values, incorrect prediction, or timeout

### Test Data
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

### Expected Response
```json
{
  "risk_level": "medium",
  "confidence_score": 0.78,
  "reasoning": "Patient has diabetes and elevated BMI, with borderline high blood pressure",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## TC-MODEL-002: Risk Classification Model - Edge Cases
**Category**: Model Robustness  
**Priority**: Medium | **Risk**: High | **Complexity**: High

### Objective
Verify that the model handles edge cases and boundary conditions appropriately without errors or incorrect predictions.

### Prerequisites
- Model endpoint is accessible
- Edge case test data prepared (missing optional fields, boundary values)

### Test Steps
1. Test with minimal required fields only (age and gender only)
2. Test with boundary age values (0, 18, 65, 100)
3. Test with empty medical history
4. Test with extreme vitals (very high/low values)
5. Verify model responds appropriately to each case
6. Verify no crashes or errors occur
7. Verify predictions are reasonable given limited data

### Expected Results
- Model accepts minimal input without errors
- For minimal data (no medical history):
  - Risk prediction defaults appropriately (usually "low")
  - Confidence score reflects uncertainty (< 0.5)
  - Reasoning indicates "limited data available"
- Boundary age values handled correctly:
  - Age 0-17: Appropriate pediatric consideration
  - Age 65+: Age-related risk factors considered
  - Age 100+: Very high age risk reflected
- Empty medical history accepted, not treated as error
- Extreme vitals trigger appropriate high risk warnings
- No 500 errors or crashes
- Response times remain acceptable (< 3 seconds)

### Pass/Fail Criteria
- **Pass**: All edge cases handled gracefully, reasonable predictions, no errors
- **Fail**: Crashes, errors, nonsensical predictions, or timeout

### Test Data - Minimal Input
```json
{
  "patient": {
    "age": 30,
    "gender": "female"
  }
}
```

### Test Data - Extreme Values
```json
{
  "patient": {
    "age": 95,
    "gender": "male",
    "medical_history": ["heart_disease", "diabetes", "copd", "kidney_disease"],
    "vitals": {
      "blood_pressure": "180/110",
      "heart_rate": 120,
      "bmi": 35
    }
  }
}
```

---

## TC-MODEL-003: Sentiment Analysis Model - Patient Text Input
**Category**: Model Accuracy  
**Priority**: Medium | **Risk**: Medium | **Complexity**: Medium

### Objective
Validate that the sentiment analysis model correctly analyzes patient-provided text and identifies emotional tone, concerns, and urgency.

### Prerequisites
- Sentiment analysis model endpoint is accessible
- Test patient statements prepared (various sentiment types)

### Test Steps
1. Prepare patient text input expressing concern
2. Send POST request to sentiment analysis endpoint
3. Verify request is accepted (HTTP 200)
4. Verify response contains sentiment classification
5. Verify confidence score is provided
6. Verify key themes/concerns are extracted
7. Verify urgency level is assessed
8. Test with various sentiment types (positive, negative, neutral, urgent)

### Expected Results
- HTTP 200 status code returned
- Response time < 2 seconds
- Response contains:
  - `sentiment`: enum (positive, negative, neutral, concerned, urgent)
  - `confidence_score`: float [0-1]
  - `key_themes`: array of identified concerns
  - `urgency_level`: enum (low, medium, high)
  - `summary`: brief interpretation
- For urgent/concerning text, urgency flagged appropriately
- For positive text, positive sentiment identified
- Key medical terms and symptoms extracted to themes
- Consistent results for repeated analysis of same text

### Pass/Fail Criteria
- **Pass**: Correct sentiment identified, key themes extracted, urgency assessed appropriately
- **Fail**: Incorrect sentiment, missing themes, wrong urgency level

### Test Data - Concerning Text
```json
{
  "patient_text": "I've been experiencing severe chest pain for the past 2 hours. It's getting worse and I'm having trouble breathing. Should I be worried?"
}
```

### Expected Response
```json
{
  "sentiment": "urgent",
  "confidence_score": 0.92,
  "key_themes": ["chest pain", "difficulty breathing", "severe symptoms"],
  "urgency_level": "high",
  "summary": "Patient reports severe chest pain and breathing difficulty - immediate medical attention recommended"
}
```

### Test Data - Positive Text
```json
{
  "patient_text": "I'm feeling much better after starting the new medication. My symptoms have improved significantly and I have more energy throughout the day."
}
```

### Expected Response
```json
{
  "sentiment": "positive",
  "confidence_score": 0.88,
  "key_themes": ["medication effectiveness", "symptom improvement", "increased energy"],
  "urgency_level": "low",
  "summary": "Patient reports positive response to treatment with symptom improvement"
}
```

---

## Suggested Additional Test Scenarios

### TC-MODEL-004: Invalid Input Format Handling
Test model behavior with malformed JSON, missing required fields, and wrong data types. Expected: HTTP 400 error with specific validation message indicating which fields are invalid, no server crashes or 500 errors.

### TC-MODEL-005: Model Response Time Under Load
Measure response times under concurrent load (50+ simultaneous requests). Expected: 95th percentile response time remains under 2 seconds, no timeout errors, all requests processed successfully.

---

## Test Environment Requirements
- **Model Endpoints**: Accessible in test environment
- **Test Data**: Diverse patient scenarios with known expected outcomes
- **Performance Tools**: Ability to measure response times and concurrent load
- **Logging**: Access to model inference logs for debugging

## Automation Notes
Automated tests use pytest with mocking:
- `@patch` decorators to mock model API calls
- `Mock` objects to simulate model responses
- Response validation using pydantic models
- Performance timing using pytest-timeout

See: `tests/model_integration/test_risk_classification.py`
