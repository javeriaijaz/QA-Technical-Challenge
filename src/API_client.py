import os
from playwright.sync_api import APIRequestContext
from utils.logger import get_logger

logger = get_logger()
#Loading the API URL from env file
BASE_URL = os.getenv("API_BASE_URL", "https://ipwho.is")

def get_api_data(ip: str, request_context: APIRequestContext):
    try:
        response = request_context.get(f"/{ip}")

        if not response.ok:
            logger.error(f"[{ip}] API response status: {response.status}")
            return {
                "ip": ip,
                "success": False,
                "message": f"HTTP Error: {response.status}"
            }

        data = response.json()

        if not data.get("success", True):
            logger.warning(f"[{ip}] API returned unsuccessful status: {data.get('message')}")
            return {
                "ip": ip,
                "success": False,
                "message": data.get("message", "Unknown API error")
            }

        return data

    except Exception as e:
        logger.exception(f"Exception while fetching IP data for {ip}")
        return {
            "ip": ip,
            "success": False,
            "message": f"Exception occurred: {str(e)}"
        }
