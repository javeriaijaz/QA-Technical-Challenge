
# QA Automation – Technical Challenge

## Overview
This project is a Python-based test automation framework designed to validate data fetched from an external IP information API. The expected data for various test scenarios is stored in a CSV file, and test results are generated in an HTML report.

The goal is to ensure the accuracy, completeness, and consistency of the data returned by the API by validating it against different real-world and edge-case scenarios.

---

## What This Covers (Based on Assignment Instructions)

### 1. Test Automation for External API with Expected CSV Values
- Validates actual API data against the expected values row by row.
- Uses the IP as a unique key to query the API.
- Parametrized test cases ensure scalability and maintainability.

### 2. Explanation About the Solution
- Implemented in Python using `pytest`.
- Reads a CSV containing IP data and expected results for each scenario.
- Each scenario is validated using a centralized parametrized function.
- Logs detailed test information using a custom logger utility.
- Generates a standalone HTML test report using `pytest-html`.

### 3. Present the Test Results
- `report.html` is generated automatically after test execution.
- GitHub Actions CI runs the tests and uploads the report as an artifact.

### 4. Assumptions Made
- The API always returns a JSON response with field names that exactly match the headers in the `expected.csv`.
- Each IP address in the CSV uniquely identifies a test scenario and is used to query the API.
- For invalid or malformed IPs, the API might return `None` or only a partial response.
- Fields like `continent`, `postal`, `latitude`, etc., may be missing for some IPs—this is expected and tested.
- The API’s behavior is assumed stable and not affected by regional changes or rate limiting during test execution.
- The `scenario` column reliably indicates which validation logic to apply per row.
- The data in `expected.csv` is considered ground truth for validating results.

---

## Test Environment
- **Language:** Python 3.11
- **Framework:** `pytest`, `pytest-html`
- **CI/CD:** GitHub Actions
- **Operating System (CI):** Ubuntu-latest

---

## Project Structure
```
QA-Technical-Challenge/
├── .github/workflows/
│   └── run-tests.yml         # GitHub Actions workflow configuration
├── data/
│   └── expected.csv          # Input file containing test scenarios
├── src/
│   └── API_client.py         # Logic to fetch API response
├── tests/
│   └── test_validation.py    # Parametrized test suite
├── utils/
│   └── logger.py             # Utility for centralized logging
├── requirements.txt          # Python dependencies
├── report.html               # Generated HTML test report
├── test_results.log          # Execution logs
└── README.md
```

---

## Test Scenarios Covered
Test scenarios are defined in `expected.csv`, including:

- Valid IP with all fields correctly returned
- Field mismatches (e.g., country, region, city, postal)
- Edge cases such as:
  - Maximum field lengths
  - Lowercase or malformed country codes
  - Missing values (latitude, longitude, etc.)
  - Invalid IPs or unresolvable addresses
  - Out-of-range geographical values
  - Logically inconsistent values (e.g., country vs. country code)

Each row is tested dynamically using `pytest.mark.parametrize` for extensibility.

---

## How to Run Locally

### 1. Install Python 3.11+

### 2. (Optional) Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run tests
```bash
pytest tests/test_validation.py --html=report.html --self-contained-html -v
```

### 5. Open report
Open `report.html` in any browser to inspect test results.

---

## GitHub Actions CI Integration
This repository includes a GitHub Actions workflow that:
- Installs dependencies
- Runs the test suite
- Generates a report
- Uploads `report.html` as an artifact

You can trigger it manually via `Actions > Run Workflow` on GitHub.

---

## Sample `expected.csv` Entry
```csv
ip,country,region,city,country_code,continent,latitude,longitude,postal,scenario
8.8.8.8,United States,California,Mountain View,US,North America,37.3860517,-122.0838511,94039,Valid IP
8.8.8.8,Germany,California,Mountain View,US,North America,37.3860517,-122.0838511,94039,Country mismatch
```

---

## Future Improvements

- **Parallel Execution with `pytest-xdist`**  
  Enables faster execution for large datasets by distributing tests across multiple CPUs.

- **Chunked or Streaming CSV Reader**  
  Avoid loading the entire file into memory for very large datasets.

- **API Throttling Handling**  
  Add retry mechanisms, exponential backoff, or token bucket rate-limiting logic to gracefully handle API limits.

- **Domain-Based Test Inputs**  
  Extend the framework to work with other identifiers like domains or URLs instead of only IPs.

- **Advanced Data Matching**  
  Integrate fuzzy matching or NLP tools to catch near-matches or misspellings.

- **Schema-Based Validation**  
  Use libraries like `pydantic` to enforce types and formats on API responses.

- **Environment Switching**  
  Add support for switching between staging and production APIs with environment flags.

- **Fail Notification System**  
  Integrate Slack, email, or webhook-based alerts on CI failure.

- **Mock Server Integration**  
  Enable running tests offline or against controlled test data.

