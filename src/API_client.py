import requests

def get_ip_data(ip: str) -> dict | None:
    """Fetch data from ipwho.is for the given IP. Returns None on error or failure."""
    url = f"https://ipwho.is/{ip}"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()
        if not data.get("success", True):
            return None
        return {
            "country": data.get("country"),
            "region": data.get("region"),
            "city": data.get("city"),
            "country_code": data.get("country_code"),
            "continent": data.get("continent"),
            "latitude": str(data.get("latitude")),
            "longitude": str(data.get("longitude")),
            "postal": str(data.get("postal"))
        }
    except (requests.RequestException, ValueError):
        return None
