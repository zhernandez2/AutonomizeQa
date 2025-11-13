# Performance Test Cases

## Overview

This document outlines performance test cases for the Autonomize AI platform. These test cases focus on response times, latency, and throughput to ensure the system meets performance requirements for production use.

---

## Test Case Classification

- **🟡 Manual**: Requires manual execution and verification
- **🟢 Semi-Automated**: Can be partially automated with manual verification
- **🔵 Automated**: Fully automated (if tools are available)

---

## Performance Test Cases

### TC-PERF-001: Agent Response Time Under Normal Load
**Status**: 🟡 **Manual**  
**Priority**: High | **Risk**: Medium

**Objective**: Verify agent response times meet performance requirements under normal operational load

**Prerequisites**:
- Agent configured and running
- Claims system accessible
- Performance monitoring tools available
- Test data prepared (100+ claims)

**Test Steps**:
1. Measure baseline response time for single claim extraction (5 samples, average)
2. Execute 50 sequential claim extractions, measure each response time
3. Calculate statistics:
   - Average response time
   - Median response time
   - 95th percentile response time
   - 99th percentile response time
   - Minimum and maximum response times
4. Execute 50 concurrent claim extractions, repeat measurements
5. Monitor system resources (CPU, memory, network)

**Expected Results**:
- Single claim extraction: Average < 2 seconds
- Sequential extractions: 95th percentile < 3 seconds
- Concurrent extractions: 95th percentile < 5 seconds
- No response time degradation > 50% from baseline
- CPU usage < 80% during load
- Memory usage stable (no leaks)

**Pass/Fail Criteria**:
- **Pass**: All response times meet thresholds, stable resource usage
- **Fail**: Response times exceed thresholds or resource usage unstable

**Tools**:
- Performance monitoring: `time` command, custom timing scripts
- Load generation: Custom scripts, Apache Bench, Locust
- Resource monitoring: `top`, `htop`, system monitoring tools

**Example Test Scripts**:

**Using curl (sequential test)**:
```bash
# Sequential test
for i in {1..50}; do
  time curl -X GET http://localhost:8000/api/v1/agent/claims-system/CLM001
done
```

**Using Apache Bench (concurrent test)**:
```bash
ab -n 50 -c 10 http://localhost:8000/api/v1/agent/claims-system/CLM001
```

**Using Locust**:
Create `locustfile_agent.py`:
```python
from locust import HttpUser, task, between
import json

class AgentUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    @task
    def extract_claim(self):
        claim_ids = ["CLM001", "CLM002", "CLM003", "CLM004", "CLM005"]
        claim_id = claim_ids[self.environment.runner.user_count % len(claim_ids)]
        self.client.get(f"/api/v1/agent/claims-system/{claim_id}", name="/agent/claims-system/[claim_id]")
```

Run Locust:
```bash
# Install Locust: pip install locust
# Start Locust web UI
locust -f locustfile_agent.py --host=http://localhost:8000

# Or run headless (no UI)
locust -f locustfile_agent.py --host=http://localhost:8000 --headless -u 50 -r 10 -t 5m
# -u: number of users
# -r: spawn rate (users per second)
# -t: test duration
```

---

### TC-PERF-002: Model Inference Latency
**Status**: 🟡 **Manual**  
**Priority**: High | **Risk**: High

**Objective**: Verify AI model inference times meet requirements for real-time decision support

**Prerequisites**:
- Model endpoints accessible
- Test data prepared
- Performance measurement tools

**Test Steps**:
1. Measure baseline inference time for risk classification (100 samples)
2. Measure baseline inference time for sentiment analysis (100 samples)
3. Calculate statistics:
   - Average latency
   - P50, P95, P99 percentiles
   - Standard deviation
4. Test with various input sizes:
   - Minimal input (age + gender only)
   - Standard input (full patient data)
   - Large input (extended medical history)
5. Test under concurrent load (10, 50, 100 concurrent requests)

**Expected Results**:
- Risk Classification:
  - Average < 1.5 seconds
  - P95 < 2 seconds
  - P99 < 3 seconds
- Sentiment Analysis:
  - Average < 1 second
  - P95 < 1.5 seconds
  - P99 < 2 seconds
- Latency increases < 20% under concurrent load
- No timeout errors

**Pass/Fail Criteria**:
- **Pass**: All latency metrics meet thresholds, graceful degradation under load
- **Fail**: Latency exceeds thresholds or significant degradation under load

**Tools**:

**Using curl (baseline measurement)**:
```bash
# Example timing script for risk classification
for i in {1..100}; do
  time curl -X POST http://localhost:8000/api/v1/models/risk-classification \
    -H "Content-Type: application/json" \
    -d @test_data.json
done

# Example timing script for sentiment analysis
for i in {1..100}; do
  time curl -X POST http://localhost:8000/api/v1/models/sentiment-analysis \
    -H "Content-Type: application/json" \
    -d @sentiment_test_data.json
done
```

**Using Apache Bench (concurrent load test)**:
```bash
ab -n 100 -c 10 -p test_data.json -T application/json \
  http://localhost:8000/api/v1/models/risk-classification
```

**Using Locust**:
Create `locustfile_models.py`:
```python
from locust import HttpUser, task, between
import json

class ModelUser(HttpUser):
    wait_time = between(0.5, 2)  # Wait 0.5-2 seconds between requests
    
    # Risk classification test data
    risk_classification_data = {
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
    
    # Sentiment analysis test data
    sentiment_data = {
        "patient_text": "I've been experiencing severe chest pain for the past 2 hours. It's getting worse and I'm having trouble breathing."
    }
    
    @task(3)  # 3x more likely than sentiment analysis
    def risk_classification(self):
        self.client.post(
            "/api/v1/models/risk-classification",
            json=self.risk_classification_data,
            name="/models/risk-classification"
        )
    
    @task(1)
    def sentiment_analysis(self):
        self.client.post(
            "/api/v1/models/sentiment-analysis",
            json=self.sentiment_data,
            name="/models/sentiment-analysis"
        )
```

Run Locust:
```bash
# Install Locust: pip install locust
# Start Locust web UI
locust -f locustfile_models.py --host=http://localhost:8000

# Or run headless with specific load
locust -f locustfile_models.py --host=http://localhost:8000 --headless -u 100 -r 20 -t 10m
# -u: number of concurrent users
# -r: spawn rate (users per second)
# -t: test duration (10 minutes)
```

**Locust Web UI Features**:
- Real-time statistics dashboard
- Response time percentiles (P50, P95, P99)
- Request rate and failure rate
- Export results to CSV
- Interactive load control (start/stop/ramp up users)

**Test Data Examples**:

**Minimal Input** (for risk classification):
```json
{
  "patient": {
    "age": 30,
    "gender": "female"
  }
}
```

**Standard Input** (for risk classification):
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

**Sentiment Analysis Input**:
```json
{
  "patient_text": "I've been experiencing severe chest pain for the past 2 hours. It's getting worse and I'm having trouble breathing."
}
```

---

### TC-PERF-003: Throughput Testing
**Status**: 🟡 **Manual**  
**Priority**: Medium | **Risk**: Medium

**Objective**: Verify system can handle required transaction throughput

**Prerequisites**:
- System configured for production-like environment
- Load testing tools available
- Baseline throughput requirements defined

**Test Steps**:
1. Measure maximum throughput for agent (requests per second)
2. Measure maximum throughput for models (requests per second)
3. Test sustained throughput over 1 hour period
4. Monitor for:
   - Throughput degradation over time
   - Error rate increase
   - Resource exhaustion
5. Test peak load scenarios (2x normal throughput for 10 minutes)

**Expected Results**:
- Agent: Minimum 10 requests/second sustained
- Models: Minimum 20 requests/second sustained
- Error rate < 1% under sustained load
- No throughput degradation > 10% over 1 hour
- System recovers gracefully after peak load

**Pass/Fail Criteria**:
- **Pass**: Throughput meets requirements, stable under sustained load
- **Fail**: Throughput below requirements or significant degradation

**Tools**:

**Using Apache Bench (quick throughput test)**:
```bash
# Agent throughput test
ab -n 1000 -c 20 http://localhost:8000/api/v1/agent/claims-system/CLM001

# Model throughput test
ab -n 2000 -c 20 -p test_data.json -T application/json \
  http://localhost:8000/api/v1/models/risk-classification
```

**Using Locust**:
Create `locustfile_throughput.py`:
```python
from locust import HttpUser, task, between
import json

class ThroughputUser(HttpUser):
    wait_time = between(0.1, 0.5)  # Minimal wait for maximum throughput
    
    claim_ids = ["CLM001", "CLM002", "CLM003", "CLM004", "CLM005"]
    risk_data = {
        "patient": {
            "age": 45,
            "gender": "male",
            "medical_history": ["diabetes"],
            "vitals": {"blood_pressure": "140/90", "heart_rate": 82, "bmi": 28}
        }
    }
    
    @task(2)
    def agent_extraction(self):
        claim_id = self.claim_ids[self.environment.runner.user_count % len(self.claim_ids)]
        self.client.get(f"/api/v1/agent/claims-system/{claim_id}", name="/agent/claims-system/[claim_id]")
    
    @task(3)
    def risk_classification(self):
        self.client.post("/api/v1/models/risk-classification", json=self.risk_data, name="/models/risk-classification")
```

Run sustained load test (1 hour):
```bash
# Install Locust: pip install locust
# Run 1-hour sustained load test
locust -f locustfile_throughput.py --host=http://localhost:8000 --headless -u 50 -r 10 -t 1h

# Monitor in real-time (run in separate terminal)
# Locust web UI provides live statistics
locust -f locustfile_throughput.py --host=http://localhost:8000
# Then open http://localhost:8089 in browser

# Export results
locust -f locustfile_throughput.py --host=http://localhost:8000 --headless -u 50 -r 10 -t 1h --csv=throughput_results
# Generates: throughput_results_stats.csv, throughput_results_failures.csv
```

**Locust Features**:
- Real-time monitoring of requests/second
- Automatic calculation of throughput metrics
- Ability to ramp up/down load dynamically
- Detailed statistics and CSV export
- Supports long-duration tests (1+ hours)
- Can simulate realistic user behavior patterns

**Monitoring During Test**:
- Track requests/second over time (Locust dashboard shows this in real-time)
- Monitor error rate (should remain < 1%) - Locust tracks failures automatically
- Monitor CPU and memory usage (use system monitoring tools)
- Track response time percentiles (Locust shows P50, P95, P99)
- Monitor for timeout errors (Locust reports timeout failures)

**Locust Monitoring Features**:
- Real-time requests/second graph
- Response time distribution chart
- Failure rate tracking
- Response time percentiles (P50, P95, P99, min, max)
- Export statistics to CSV for analysis

---

## Performance Test Summary

### Test Case Distribution

- **TC-PERF-001**: Agent Response Time Under Normal Load
- **TC-PERF-002**: Model Inference Latency
- **TC-PERF-003**: Throughput Testing

**Total Performance Test Cases**: 3

### Performance Targets Summary

| Component | Metric | Target |
|-----------|--------|--------|
| Agent | Single request | < 2 seconds |
| Agent | Sequential (P95) | < 3 seconds |
| Agent | Concurrent (P95) | < 5 seconds |
| Agent | Throughput | ≥ 10 req/sec |
| Risk Classification | Average latency | < 1.5 seconds |
| Risk Classification | P95 latency | < 2 seconds |
| Risk Classification | P99 latency | < 3 seconds |
| Risk Classification | Throughput | ≥ 20 req/sec |
| Sentiment Analysis | Average latency | < 1 second |
| Sentiment Analysis | P95 latency | < 1.5 seconds |
| Sentiment Analysis | P99 latency | < 2 seconds |
| Sentiment Analysis | Throughput | ≥ 20 req/sec |

### Execution Priority

1. **High Priority** (Execute First):
   - TC-PERF-001: Agent Response Time
   - TC-PERF-002: Model Inference Latency

2. **Medium Priority**:
   - TC-PERF-003: Throughput Testing

---

## Document Version

- **Version**: 1.0
- **Last Updated**: 2024-01-15
- **Focus**: Performance testing only
