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

# Add Gear Tests

def test_add_gear_creates_item_with_auto_id(client, tmp_path, monkeypatch):
    """
    POST /add_gear should create a new item in gear_items.json for the given class,
    auto-assigning ID when user does not provide one.
    """
    # Point to temporary files
    tmp_class_path = tmp_path / "user_classes.json"
    tmp_gear_path = tmp_path / "gear_items.json"
    monkeypatch.setattr(app_module, "classPath", str(tmp_class_path), raising=False)
    monkeypatch.setattr(app_module, "gearPath", str(tmp_gear_path), raising=False)

    # Set up in-memory class definition and persist it so app_module.userClasses is consistent
    app_module.userClasses = {
        "Helmet": {
            "fields": [
                {"name": "ID", "type": "number"},
                {"name": "Size", "type": "text"},
            ]
        }
    }
    # We don't need to write user_classes.json here because addGear uses userClasses in memory,
    # but we ensure gear_items.json starts as empty dict.
    tmp_gear_path.write_text(json.dumps({}))

    # Submit form to add a gear item
    response = client.post(
        "/add_gear",
        data={
            "class_name": "Helmet",
            # field 0: ID (left blank, so it should auto-generate)
            "fieldname_0": "ID",
            "field_0": "",
            # field 1: Size
            "fieldname_1": "Size",
            "field_1": "M",
        },
        follow_redirects=False,
    )

    # After successful add, route redirects to dashboard
    assert response.status_code == 302

    # Verify gear_items.json now has one Helmet item with ID=1, Size="M"
    data = json.loads(tmp_gear_path.read_text())
    assert "Helmet" in data
    items = data["Helmet"]
    assert len(items) == 1
    assert items[0]["ID"] == 1
    assert items[0]["Size"] == "M"

# Edit Gear Tests

def test_edit_gear_updates_existing_item(client, tmp_path, monkeypatch):
    """
    POST /edit_gear should update an existing item in gear_items.json.
    """
    # Point to temporary files
    tmp_class_path = tmp_path / "user_classes.json"
    tmp_gear_path = tmp_path / "gear_items.json"
    monkeypatch.setattr(app_module, "classPath", str(tmp_class_path), raising=False)
    monkeypatch.setattr(app_module, "gearPath", str(tmp_gear_path), raising=False)

    # Set up class definition in memory
    app_module.userClasses = {
        "Helmet": {
            "fields": [
                {"name": "ID", "type": "number"},
                {"name": "Size", "type": "text"},
            ]
        }
    }

    # Existing gear item in JSON
    initial_gear = {
        "Helmet": [
            {"ID": 1, "Size": "M"},
        ]
    }
    tmp_gear_path.write_text(json.dumps(initial_gear))

    # Submit edit form to change Size from M to L
    response = client.post(
        "/edit_gear",
        data={
            "class_name": "Helmet",
            "item_id": "1",
            # fields must match order in userClasses
            "fieldname_0": "ID",
            "field_0": "1",
            "fieldname_1": "Size",
            "field_1": "L",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302  # redirects to dashboard

    # Verify item was updated in JSON
    data = json.loads(tmp_gear_path.read_text())
    items = data["Helmet"]
    assert len(items) == 1
    assert items[0]["ID"] == 1
    assert items[0]["Size"] == "L"

# view items test

def test_view_items_displays_items_for_class(client, tmp_path, monkeypatch):
    """
    GET /view_items?class_name=Helmet should render a page containing that class's items.
    """
    # Point to temporary gear JSON
    tmp_gear_path = tmp_path / "gear_items.json"
    monkeypatch.setattr(app_module, "gearPath", str(tmp_gear_path), raising=False)

    # Create some sample items
    gear_data = {
        "Helmet": [
            {"ID": 1, "Size": "M"},
            {"ID": 2, "Size": "L"},
        ]
    }
    tmp_gear_path.write_text(json.dumps(gear_data))

    # Request items for Helmet
    response = client.get("/view_items?class_name=Helmet", follow_redirects=False)
    assert response.status_code == 200

    # Check that the HTML includes the class name and some item values
    html = response.data.decode("utf-8")
    assert "Helmet" in html
    assert "1" in html
    assert "M" in html
    assert "2" in html
    assert "L" in html