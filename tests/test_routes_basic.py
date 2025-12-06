# Tests in this file were generated with assistance from an AI tool (ChatGPT)
# based on the current version of test.py (Flask app for the inventory system).

import os
import sys
import pytest

# --- Make sure Python can see app.py in the project root ---

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app as flask_app  # this expects app.py in the project root

@pytest.fixture
def client():
    """Provide a Flask test client for each test."""
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "dev-secret-key"

    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

def test_home_redirects_to_login(client):
    """
    GET / should always redirect to /login.
    This tests the 'home' route.
    """
    response = client.get("/", follow_redirects=False)

    # Expect a 302 redirect
    assert response.status_code == 302
    # Location header should end with /login
    assert "/login" in response.headers["Location"]