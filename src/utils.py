def compare_fields(expected: dict, actual: dict, fields: list) -> dict:
    """Return a dict of field mismatches: field -> (expected, actual)."""
    mismatches = {}
    for field in fields:
        exp_val = expected.get(field)
        act_val = actual.get(field)
        if str(exp_val).strip() != str(act_val).strip():
            mismatches[field] = (exp_val, act_val)
    return mismatches
