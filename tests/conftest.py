import pytest
import database.db as db_module
from database.db import init_db
import app as flask_app_module


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email="test@example.com", password="password123"):
        return self._client.post("/login", data={"email": email, "password": password})


@pytest.fixture
def app(monkeypatch, tmp_path):
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr(db_module, "DB_PATH", test_db)
    init_db()
    flask_app_module.app.config["TESTING"] = True
    flask_app_module.app.config["SECRET_KEY"] = "test-secret"
    yield flask_app_module.app


@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c


@pytest.fixture
def auth(client):
    return AuthActions(client)
