# QA Automation – Technical Challenge (Python + Playwright Variant)

## Overview
This project is a Python-based test automation framework that uses **Playwright’s API testing capabilities** combined with `pytest` to validate data fetched from the IP geolocation API `ipwho.is`. The expected data is stored in a CSV file and verified against real API responses. The results are output as an HTML test report.

This hybrid setup demonstrates a clean and scalable API testing framework using modern browser automation tools (Playwright)

---

## Two Solution Variants

This project demonstrates **two approaches** to solving the same problem:

- **Playwright-based API Testing** (Main branch)  
  Uses Playwright’s `APIRequestContext` to simulate API calls as if triggered from a browser.  
  _Useful for testing browser-originated API requests or enforcing CORS/security testing._
  
  Scalable: This setup can be easily extended to include UI automation tests alongside API validations, enabling full-stack end-to-end testing within the same framework.

- **Requests-based Classic Testing** (see `just-python-variant` branch)  
  Uses Python’s standard `requests` library for simple API validations.  
  _Faster setup and simpler logic for purely backend/API-focused testing._

---

## Features

- Hybrid Python + Playwright API testing framework
- Parametrized test execution with dynamic scenario labeling
- Field-level validation of structured API responses
- Centralized logging for traceability and debugging
- HTML report generation via `pytest-html`
- CI integration via GitHub Actions
- Easy environment switching via `.env` config

---

## What This Covers (Based on Assignment Instructions)

### 1. Test Automation for External API with Expected CSV Values
- Queries the API using IP addresses as keys.
- Validates API responses field-by-field against expected values from `expected.csv`.
- Uses `pytest.mark.parametrize` for scalable test cases.
- Uses `Playwright` under the hood instead of `requests`.

### 2. Why This API Was Chosen
The `ipwho.is` API was chosen due to its:
- Public availability (no auth needed)
- Detailed geolocation output (IP, city, region, country, etc.)
- Relevance to the **Forescout domain**, which focuses on **network visibility, IP-level intelligence, and device classification**.

### 3. Explanation About the Solution
- Built with Python 3.11+
- Uses `Playwright` for API calls.
- Custom validation logic organized per scenario (e.g., country mismatch, invalid IP).
- Configurable via `.env` file for base URL overrides.
- Generates HTML reports with `pytest-html`.
- GitHub Actions runs the tests and uploads results automatically.

### 4. Present the Test Results
- `report.html` is auto-generated after test runs.
- CI run artifacts include both logs and HTML reports.

### 5. Assumptions Made
- Every row in `expected.csv` contains an IP and a scenario label.
- Since there’s no fixed schema or validation criteria provided, I assumed each row in the CSV represents a different test case or scenario — and that I'm free to define what constitutes "valid" or "invalid" in each case.
- It wasn’t clear how extensive the test scenarios should be, so I aimed to cover both happy paths and edge cases (e.g.,    invalid IPs, missing fields, mismatched values) based on what a QA team might actually care about in production.
- No mention of which tools or frameworks to use, so I went with Python + pytest because of its readability, ecosystem, and good support for CI — and added Playwright for its request API (as an alternative to requests) to show extensibility.
- I assumed that structured output and reporting were expected, even if not stated, so I built in HTML reports and logging to demonstrate test visibility and traceability.
- The phrase “validate against expected values” didn’t restrict how deep the comparison should be (e.g., strict vs fuzzy match), so I built strict equality checks while leaving room to extend to more advanced logic (e.g., fuzzy matching, range validation).
- There was no restriction on file structure or test style, so I modularized it into clean components (validators, logger, test runner) as I would in a real project

---

## Test Environment
- **Language:** Python 3.11
- **Framework:** Playwright + Pytest
- **Reporting:** `pytest-html`
- **CI/CD:** GitHub Actions
- **Playwright Runtime:** Headless context (API-only mode)

---

## Project Structure
```
forescout_qa_solution/
├── .github/workflows/test.yml                         
├── data/expected.csv              
├── src/API_client.py             
├── tests/
│   ├── conftest.py
│   └── test_validation.py        
├── validators/scenarios.py       
├── utils/logger.py               
├── requirements.txt          
├── report.html                
├── test_results.log            
```

---

## Test Scenarios Covered

Examples include:

- Valid IP – all fields matched  
- Country mismatch  
- Region or city mismatch  
- Missing or empty fields (e.g. postal, lat/lng)  
- Malformed IPs or reserved ranges  
- Logical inconsistencies (e.g., continent vs country code)

All are tagged via the `scenario` column in `expected.csv`.

---

## How to Run Locally

### 1. Install Python 3.11+

### 2. Set up virtual environment (optional)
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 4. Add environment variable (optional)
Create a `.env` file (already ignored from Git) like:
```
BASE_URL=https://ipwho.is
```

### 5. Run the tests
```bash
pytest tests/test_validation.py --html=report.html --self-contained-html -v
```

---

## GitHub Actions CI Integration

CI/CD Pipeline:
- Installs Python and Playwright
- Loads BASE_URL from GH secrets
- Runs tests
- Uploads `report.html` and logs as artifacts

Check the **Actions** tab for workflows.

---

## Sample `expected.csv` Entry
```csv
ip,country,region,city,country_code,continent,latitude,longitude,postal,scenario
8.8.8.8,United States,California,Mountain View,US,North America,37.3860517,-122.0838511,94039,Valid IP
8.8.8.8,Germany,California,Mountain View,US,North America,37.3860517,-122.0838511,94039,Country mismatch
```

---

## Future Improvements

- **Support for Authorized APIs**
  Extend the framework to handle APIs that require authentication (e.g., API keys, bearer tokens, OAuth). This would involve configuring headers or tokens via environment variables and securely injecting them during test execution. While a public API was chosen for simplicity, integrating a secured API would make the solution more production-ready.

- **Parallel Execution with `pytest-xdist`**  
  Use pytest-xdist to run tests in parallel using all CPU cores. This can significantly reduce execution time for large datasets.

- **Allure Reporting Integration**
  Use Allure for richer, interactive test reports with visual steps, attachments, and trends over time.

- **Chunked or Streaming CSV Reader**  
  Switch from reading the whole CSV at once to a streaming/chunked approach for memory efficiency with large files.

- **API Throttling Handling**  
  Add retry logic with exponential backoff to prevent tests from failing due to temporary network or rate-limit issues.

- **Domain-Based Test Inputs**  
  Extend tests to work with other keys (like domain names or user IDs) instead of only IPs.

- **Environment Switching**  
  Support testing against staging vs production API by using config flags or environment variables.

- **Fail Notification System**  
  Integrate Slack, email, or webhook-based alerts on CI failure.

- **Mock Server Integration**  
  Create a mock server to simulate API responses locally—useful for offline testing or developing without hitting the live API.
