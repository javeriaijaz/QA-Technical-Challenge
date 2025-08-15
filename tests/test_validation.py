import csv
import pytest
from src.API_client import get_ip_data
from src.logger_util import get_logger

CSV_FILE_PATH = "data/expected.csv"
logger = get_logger()

# Load all rows from the expected.csv file into memory
def load_test_cases():
    with open(CSV_FILE_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# Parametrize the test using the "scenario" column for better readability in reports
@pytest.mark.parametrize("row", load_test_cases(), ids=lambda r: r["scenario"])
def test_ip_data_validation(row):
    scenario = row["scenario"].strip().lower()
    actual = get_ip_data(row["ip"])

    logger.info(f"[{scenario}] Testing IP: {row['ip']}")

    try:
        if scenario == "valid ip":
            # Compare each non-empty field with API response
            mismatches = {
                field: (row[field], str(actual.get(field)))
                for field in row
                if field in actual and row[field] != "" and str(actual.get(field)) != row[field]
            }
            if mismatches:
                logger.error(f"[{scenario}] Mismatches: {mismatches}")
            else:
                logger.info(f"[{scenario}] All fields matched")
            assert not mismatches, f"Mismatches found: {mismatches}"

        elif scenario == "country mismatch":
            assert actual.get("country") != row["country"]

        elif scenario == "region mismatch":
            assert actual.get("region") != row["region"]

        elif scenario == "city mismatch":
            assert actual.get("city") != row["city"]

        elif scenario == "country code mismatch":
            assert actual.get("country_code") != row["country_code"]

        elif scenario == "continent mismatch":
            assert actual.get("continent") != row["continent"]

        elif scenario == "invalid country":
            assert actual.get("country") != row["country"]

        elif scenario == "missing city":
            assert actual.get("city") not in [None, ""]

        elif scenario == "missing region and city":
            assert actual.get("region") not in [None, ""]
            assert actual.get("city") not in [None, ""]

        elif scenario == "missing country code":
            assert actual.get("country_code") not in [None, ""]

        elif scenario == "missing continent":
            assert actual.get("continent") not in [None, ""]

        elif scenario == "missing latitude":
            assert actual.get("latitude") not in [None, ""]

        elif scenario == "missing longitude":
            assert actual.get("longitude") not in [None, ""]

        elif scenario == "lowercase country code":
            assert actual.get("country_code") != row["country_code"]

        elif scenario == "too long country code":
            assert len(actual.get("country_code", "")) <= 2

        elif scenario == "invalid continent":
            assert actual.get("continent") != row["continent"]

        elif scenario == "latitude out of range":
            lat = float(actual.get("latitude", 0))
            assert -90 <= lat <= 90

        elif scenario == "longitude out of range":
            lon = float(actual.get("longitude", 0))
            assert -180 <= lon <= 180

        elif scenario == "postal code mismatch":
            assert actual.get("postal") != row["postal"]

        elif scenario == "missing postal":
            assert actual.get("postal") not in [None, ""]

        elif scenario == "invalid postal":
            assert actual.get("postal") != row["postal"]

        elif scenario in ["invalid ip format", "invalid ip"]:
            assert actual is None, f"Expected None for invalid IP, got: {actual}"

        elif scenario == "max length city":
            assert actual.get("city") != row["city"]

        elif scenario == "max length region":
            assert actual.get("region") != row["region"]

        elif scenario == "conflicting country and code":
            assert not (
                actual.get("country") == row["country"]
                and actual.get("country_code") == row["country_code"]
            )

        else:
            logger.warning(f"Unhandled scenario: {scenario}")
            pytest.skip(f"Scenario '{scenario}' not handled yet.")

    except AssertionError as e:
        logger.error(f"[{scenario}] Assertion failed: {str(e)}")
        raise
