import sqlite3
from collections import defaultdict
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"  # replace with env var in production

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Name is required")
    if not email or "@" not in email:
        return render_template("register.html", error="A valid email address is required")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters")

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists")
    finally:
        conn.close()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = get_db()
    row = conn.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if row is None or not check_password_hash(row["password_hash"], password):
        return render_template("login.html", error="Invalid email or password")

    session.clear()
    session["user_id"] = row["id"]
    session["name"] = row["name"]
    return redirect(url_for("profile"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db()
    expenses = conn.execute(
        "SELECT id, amount, category, date, description FROM expenses"
        " WHERE user_id = ? ORDER BY date DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    current_month = datetime.now().strftime("%Y-%m")
    total_this_month = sum(
        row["amount"] for row in expenses
        if row["date"].startswith(current_month)
    )
    expense_count = len(expenses)

    if expenses:
        cat_totals = defaultdict(float)
        for row in expenses:
            cat_totals[row["category"]] += row["amount"]
        top_category = max(cat_totals, key=cat_totals.get)
    else:
        top_category = ""

    return render_template(
        "profile.html",
        expenses=expenses,
        total_this_month=total_this_month,
        expense_count=expense_count,
        top_category=top_category,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
