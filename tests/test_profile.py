import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash
from database.db import get_db
from app import compute_profile_stats


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _create_user(email="test@example.com", password="password123", name="Test User"):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id, email, password


def _add_expense(user_id, amount, category, date, description=""):
    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description)"
        " VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, date, description),
    )
    conn.commit()
    conn.close()


# ------------------------------------------------------------------ #
# Unit tests — compute_profile_stats (no HTTP)                        #
# ------------------------------------------------------------------ #

def test_compute_stats_empty():
    stats = compute_profile_stats([])
    assert stats["total_this_month"] == 0
    assert stats["expense_count"] == 0
    assert stats["top_category"] == ""


def test_compute_stats_excludes_past_months():
    current_month = datetime.now().strftime("%Y-%m")
    expenses = [
        {"amount": 50.0, "category": "Food",      "date": f"{current_month}-01"},
        {"amount": 30.0, "category": "Transport",  "date": f"{current_month}-05"},
        {"amount": 200.0, "category": "Bills",     "date": "2020-01-10"},  # old month
    ]
    stats = compute_profile_stats(expenses)
    assert stats["total_this_month"] == pytest.approx(80.0)
    assert stats["expense_count"] == 3
    assert stats["top_category"] == "Bills"  # 200 > Food(50) > Transport(30), all-time


# ------------------------------------------------------------------ #
# Integration tests — GET /profile via test client                    #
# ------------------------------------------------------------------ #

def test_profile_redirects_when_logged_out(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert response.location.endswith("/login")


def test_profile_renders_when_logged_in(client, auth):
    _create_user()
    auth.login()
    response = client.get("/profile")
    assert response.status_code == 200


def test_profile_shows_correct_monthly_total(client, auth):
    current_month = datetime.now().strftime("%Y-%m")
    user_id, email, password = _create_user()
    _add_expense(user_id, 40.00, "Food",      f"{current_month}-01")
    _add_expense(user_id, 60.00, "Transport", f"{current_month}-10")
    _add_expense(user_id, 99.99, "Bills",     "2020-03-15")  # old month, excluded

    auth.login(email, password)
    response = client.get("/profile")

    assert response.status_code == 200
    assert "100.00" in response.get_data(as_text=True)


def test_profile_shows_correct_expense_count(client, auth):
    current_month = datetime.now().strftime("%Y-%m")
    user_id, email, password = _create_user()
    _add_expense(user_id, 10.00, "Food",     f"{current_month}-01")
    _add_expense(user_id, 20.00, "Shopping", f"{current_month}-05")
    _add_expense(user_id, 30.00, "Health",   "2019-06-20")

    auth.login(email, password)

    conn = get_db()
    expenses = conn.execute(
        "SELECT amount, category, date FROM expenses WHERE user_id = ?",
        (user_id,),
    ).fetchall()
    conn.close()

    stats = compute_profile_stats(list(expenses))
    assert stats["expense_count"] == 3


def test_profile_shows_top_category(client, auth):
    current_month = datetime.now().strftime("%Y-%m")
    user_id, email, password = _create_user()
    _add_expense(user_id, 100.00, "Food",      f"{current_month}-01")
    _add_expense(user_id,  20.00, "Transport", f"{current_month}-02")
    _add_expense(user_id,  50.00, "Food",      f"{current_month}-03")  # Food total = 150

    auth.login(email, password)
    response = client.get("/profile")

    assert response.status_code == 200
    assert "Food" in response.get_data(as_text=True)


def test_profile_empty_state(client, auth):
    _create_user()
    auth.login()
    response = client.get("/profile")
    assert response.status_code == 200
