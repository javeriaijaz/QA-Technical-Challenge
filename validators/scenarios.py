from utils.logger import get_logger

logger = get_logger()

# --------- Validators --------- #

def validate_valid_ip(actual, row):
    mismatches = {
        field: (row[field], str(actual.get(field)))
        for field in row
        if field in actual and row[field] and str(actual.get(field)) != row[field]
    }
    if mismatches:
        logger.error(f"[valid ip] Mismatches: {mismatches}")
    assert not mismatches, f"Mismatches found: {mismatches}"

def validate_field_not_equal(field):
    def validator(actual, row):
        assert actual.get(field) != row[field], f"{field} should not match"
    return validator

def validate_field_present(field):
    def validator(actual, _):
        assert actual.get(field) not in [None, ""], f"{field} should be present"
    return validator

def validate_latitude_range(actual, _):
    try:
        lat = float(actual.get("latitude", 0))
    except ValueError:
        raise AssertionError(f"Invalid latitude format: {actual.get('latitude')}")
    assert -90 <= lat <= 90, f"Latitude out of range: {lat}"

def validate_longitude_range(actual, _):
    try:
        lon = float(actual.get("longitude", 0))
    except ValueError:
        raise AssertionError(f"Invalid longitude format: {actual.get('longitude')}")
    assert -180 <= lon <= 180, f"Longitude out of range: {lon}"

def validate_invalid_ip(actual, _):
    assert isinstance(actual, dict), "Expected a response dictionary"
    assert actual.get("success") is False, "Expected 'success': false for invalid or restricted IP"
    message = (actual.get("message") or "").lower()
    valid_reasons = ["invalid", "reserved", "private", "broadcast", "loopback"]
    assert any(reason in message for reason in valid_reasons), f"Unexpected error message: '{message}'"

def validate_empty_ip(actual, _):
    assert actual.get("success") is False, "Expected 'success': false for empty IP"
    assert "IP address is required" in actual.get("message", "") or "Invalid IP" in actual.get("message", ""), \
        f"Unexpected error message: {actual.get('message')}"

def validate_conflicting_country_and_code(actual, row):
    assert not (
        actual.get("country") == row["country"] and
        actual.get("country_code") == row["country_code"]
    ), "Conflicting country and code should not match"

# --------- Scenario Map --------- #

SCENARIO_FUNCTIONS = {
    "valid ip": validate_valid_ip,
    "valid ipv6 address": validate_valid_ip,
    "empty ip input": validate_empty_ip,
    "country mismatch": validate_field_not_equal("country"),
    "region mismatch": validate_field_not_equal("region"),
    "city mismatch": validate_field_not_equal("city"),
    "country code mismatch": validate_field_not_equal("country_code"),
    "continent mismatch": validate_field_not_equal("continent"),
    "invalid country": validate_field_not_equal("country"),
    "missing city": validate_field_present("city"),
    "missing region and city": lambda a, r: [
        validate_field_present("region")(a, r),
        validate_field_present("city")(a, r)
    ],
    "missing country code": validate_field_present("country_code"),
    "missing continent": validate_field_present("continent"),
    "missing latitude": validate_field_present("latitude"),
    "missing longitude": validate_field_present("longitude"),
    "lowercase country code": validate_field_not_equal("country_code"),
    "too long country code": lambda a, r: (_ for _ in ()).throw(
        AssertionError("Country code too long")
    ) if len(a.get("country_code", "")) > 2 else None,
    "invalid continent": validate_field_not_equal("continent"),
    "latitude out of range": validate_latitude_range,
    "longitude out of range": validate_longitude_range,
    "invalid latitude format without decimal": validate_latitude_range,
    "invalid longitude format": validate_longitude_range,
    "postal code mismatch": validate_field_not_equal("postal"),
    "missing postal": validate_field_present("postal"),
    "invalid postal": validate_field_not_equal("postal"),
    "non-numeric postal": validate_field_not_equal("postal"),
    "no dash in zip+4": validate_field_not_equal("postal"),
    "valid postal extended": validate_valid_ip,
    "ip with port number (should be rejected)": validate_invalid_ip,
    "invalid ip": validate_invalid_ip,
    "invalid ip format": validate_invalid_ip,
    "ipv6 loopback address": validate_invalid_ip,
    "loopback ip": validate_invalid_ip,
    "private ip range": validate_invalid_ip,
    "broadcast ip address": validate_invalid_ip,
    "max length city": validate_field_not_equal("city"),
    "max length region": validate_field_not_equal("region"),
    "conflicting country and code": validate_conflicting_country_and_code
}
