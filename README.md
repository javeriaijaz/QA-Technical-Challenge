# API Data Validation Automation

This project is a Python-based test automation framework designed to validate data fetched from an external IP information API. The expected data for various test scenarios is stored in a CSV file, and test results are generated in an HTML report.

The goal is to ensure the accuracy, completeness, and consistency of the data returned by the API by validating it against different real-world and edge-case scenarios.

---

What This Covers (Based on Assignment Instructions)

1. Test Automation for External API with Expected CSV Values:

Validates actual API data against the expected values row by row.

Uses the IP as a unique key to query the API.

Uses parametrized test cases for scalability and maintainability.

2. Explanation About the Solution:

Written in Python using pytest.

The test reads a CSV with expected IP data and scenarios.

Each scenario is mapped to specific test assertions.

A logger captures detailed output per test case.

Test results are also reported in an HTML file using pytest-html.

3. Present the Test Results:

HTML report (report.html) is generated automatically after test execution.

GitHub Actions CI setup runs tests and uploads the report as an artifact.

4. Assumptions Made:

The API always returns data in JSON.

The field names in the API match the column headers in the CSV.

The IP address is treated as the primary key to fetch results.

Some negative scenarios (e.g., invalid IPs) may return None or partial data.

---

Test Stack

Language: Python 3.11

Framework: pytest + pytest-html

CI/CD: GitHub Actions

OS (CI): Ubuntu-latest

## Project Structure

```
├── data/
│   └── expected.csv              # Contains the test scenarios and expected values
├── src/
│   └── API_client.py             # Contains function to fetch actual API response
├── tests/
│   └── test_validation.py        # Main test suite covering all scenarios
├── utils/
│   └── logger.py                 # Centralized logger utility for debug output
├── requirements.txt              # All required dependencies
├── report.html                   # Generated pytest HTML report
└── .github/
    └── workflows/
        └── test.yml          # GitHub Actions CI config
```

---

## Test Scenarios

Test cases are driven from `expected.csv`, and include:

- Happy path with valid values
- Mismatches (e.g., incorrect `country`, `region`, `postal`)
- Edge cases (e.g., `max length city`, `invalid IP`)
- Missing fields (e.g., missing `latitude`, `country_code`)
- Format and range errors (e.g., out-of-range `longitude`, malformed IP)

Each row in the CSV represents a scenario, and tests are run dynamically using `pytest.mark.parametrize`.

---

## How to Run Locally

1. **Install Python 3.11+**

2. **Create virtual environment (optional)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests with HTML report**
   ```bash
   pytest tests/test_validation.py --html=report.html --self-contained-html -v
   ```

5. **View results**
   Open `report.html` in your browser.

---

## CI Integration with GitHub Actions

This repo includes a GitHub Actions workflow (`.github/workflows/api-test.yml`) to run tests automatically via:

- Manual trigger via **Actions > Run Workflow**
- Runs in `ubuntu-latest` with Python 3.11
- Uploads the HTML report as an artifact

### Run It Manually:
Go to the **Actions tab** in GitHub and click **"Run workflow"** for `Run API Validation Tests`.

---

## Sample `expected.csv` Entry

```csv
ip,country,region,city,country_code,continent,latitude,longitude,postal,scenario
8.8.8.8,United States,California,Mountain View,US,North America,37.3860517,-122.0838511,94039,Valid IP
8.8.8.8,Germany,California,Mountain View,US,North America,37.3860517,-122.0838511,94039,Country mismatch
```

---

## 📁 Logger

A custom logging utility (`utils/logger.py`) is included to track test progress and debug API responses.

---

## 📌 Future Improvements

- Add schema validation (e.g., using `pydantic`)
- Expand to other APIs or input keys (e.g., domain names)
- Generate JUnit or Allure reports for integrations
- Add automatic Slack/email notifications on failure

---

