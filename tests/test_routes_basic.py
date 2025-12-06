# Tests in this file were generated with assistance from an AI tool (ChatGPT)
# based on the current version of test.py (Flask app for the inventory system).

import os
import sys
import pytest
import json

# --- Make sure Python can see app.py in the project root ---

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app as flask_app     
import app as app_module   

@pytest.fixture
def client():
    """Provide a Flask test client for each test."""
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "dev-secret-key"

    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

# Login Tests

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

def test_dashboard_requires_login(client):
    """GET /dashboard without login should redirect to /login."""
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_sets_session_and_redirects_to_dashboard(client):
    """POST /login should set session['username'] and redirect to /dashboard."""
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "secret", "submit": "Login"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]

    # Verify that the username was stored in the session
    with client.session_transaction() as sess:
        assert sess.get("username") == "testuser"


# Create Class Tests

def test_create_class_creates_new_class_in_json(client, tmp_path, monkeypatch):
    """
    POST /create_class should create a new class entry in user_classes.json
    with an ID field plus user-defined fields.
    """
    # Point app to temporary classPath
    tmp_class_path = tmp_path / "user_classes.json"
    monkeypatch.setattr(app_module, "classPath", str(tmp_class_path), raising=False)

    # Start with empty in-memory classes
    app_module.userClasses = {}

    # Simulate form submission: class name + one extra field
    response = client.post(
        "/create_class",
        data={
            "class_name": "Helmet",
            "submit": "Create",
            "fields[0][name]": "Size",
            "fields[0][type]": "text",
        },
        follow_redirects=False,
    )

    # createClass currently returns the form page (200) even after creation
    assert response.status_code == 200

    # Verify JSON file was created and contains the new class
    assert tmp_class_path.exists()
    data = json.loads(tmp_class_path.read_text())

    assert "Helmet" in data
    fields = data["Helmet"]["fields"]
    # First field should be ID
    assert fields[0]["name"] == "ID"
    assert fields[0]["type"] == "number"
    # Second field should be our custom Size field
    assert fields[1]["name"] == "Size"
    assert fields[1]["type"] == "text"