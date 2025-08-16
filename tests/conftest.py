import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()
BASE_URL = os.getenv("API_BASE_URL", "https://ipwho.is")

@pytest.fixture(scope="session")
def request_context():
    with sync_playwright() as p:
        context = p.request.new_context(base_url=BASE_URL)
        yield context
        context.dispose()
