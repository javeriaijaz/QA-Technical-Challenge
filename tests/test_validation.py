import csv
import json
import pytest
from src.API_client import get_api_data
from utils.logger import get_logger
from validators.scenarios import SCENARIO_FUNCTIONS

CSV_FILE_PATH = "data/expected.csv"
logger = get_logger()

# Load all rows from the expected.csv file into memory
def load_test_cases():
    with open(CSV_FILE_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row.get("ip") and row.get("scenario")]

@pytest.mark.parametrize("row",load_test_cases(),ids=lambda r: r["scenario"].strip().title())
def test_ip_data_validation(row, request, request_context):
    scenario = row["scenario"].strip().lower()
    ip = row["ip"].strip()

    # Log scenario info in logs and attach full row metadata to report
    logger.info(f"[{scenario}] Testing IP: {ip}")
    request.node._report_sections.append(
        ("call", "Test Input Metadata", json.dumps(row, indent=2))
    )

    actual = get_api_data(ip, request_context)

    if actual is None:
        logger.error(f"[{scenario}] No data returned for IP: {ip}")
        pytest.fail(f"No data returned for IP: {ip}")

    try:
        validator_fn = SCENARIO_FUNCTIONS.get(scenario)
        if validator_fn:
            validator_fn(actual, row)
        else:
            logger.warning(f"Unhandled scenario: {scenario}")
            pytest.skip(f"Scenario '{scenario}' not handled yet.")
    except AssertionError as e:
        logger.error(f"[{scenario}] Assertion failed: {str(e)}")
        raise