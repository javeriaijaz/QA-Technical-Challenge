# QA Automation – Technical Challenge (Python + Playwright Variant)

## Overview
This project is a Python-based test automation framework that uses **Playwright’s API testing capabilities** combined with `pytest` to validate data fetched from the IP geolocation API `ipwho.is`. The expected data is stored in a CSV file and verified against real API responses. The results are output as an HTML test report.

This hybrid setup demonstrates a clean and scalable API testing framework using modern browser automation tools (Playwright)

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
- Fields like latitude, postal code, etc., may be missing depending on IP region.
- The `.env` file contains the `BASE_URL`, which defaults to `https://ipwho.is`.
- Each IP is treated as a unique, independent test case.

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

- **Parallel Testing** via `pytest-xdist`
- **Better CSV Handling** for huge datasets
- **Retry Mechanism** for flaky API responses
- **Domain / URL Testing** (beyond IPs)
- **pydantic Schema Validation** for strict structure checks
- **Support for Multiple Environments** via env switches
- **Slack/Webhook Fail Alerts**
- **Mock API Integration** using Playwright route mocking or local Flask server
