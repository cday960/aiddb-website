import pytest
from app import create_app
from util.crypto_utils import encrypt_string


# Fixture means this can be used in other testing functions in other files
@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app


# Gives a test client to simulate HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def fake_encrypted_password():
    return encrypt_string("fake_password123!")
