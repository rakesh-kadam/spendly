# Spec: Backend Route For Profile Page

## Overview
Step 4 delivered the `GET /profile` template and route together. This step isolates and hardens the **backend logic** of that route by writing the first pytest tests for Spendly. The profile route is the most data-rich route in the app — it queries expenses, computes three stats, and enforces authentication — making it the ideal starting point for the test suite. Students will write tests that exercise the auth guard, the database query, and the stat-computation logic, establishing patterns that every subsequent CRUD step can follow.

## Depends on
- Step 1 — Database setup (`get_db`, `init_db`, `seed_db` must be working)
- Step 2 — Registration (users can be created)
- Step 3 — Login and Logout (session stores `user_id` and `name`)
- Step 4 — Profile Page Design (`GET /profile` route and template must be complete)

## Routes
No new routes. This step tests the existing `GET /profile` route.

## Database changes
No database changes.

## Templates
- **Create:** none
- **Modify:** none

## Files to change
- `app.py` — extract the stat-computation logic (monthly total, expense count, top category) into a standalone helper function `compute_profile_stats(expenses)` so it can be unit-tested independently of the HTTP layer. The route itself calls this helper and passes the results to `render_template`.

## Files to create
- `tests/__init__.py` — empty, makes `tests/` a Python package
- `tests/conftest.py` — pytest fixtures: `app` fixture (test config, in-memory SQLite), `client` fixture (Flask test client), `auth` helper fixture for logging in
- `tests/test_profile.py` — test cases for the profile route and stat helper

## New dependencies
No new dependencies. `pytest` and `pytest-flask` are already in `requirements.txt`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- The test database must be **in-memory** (`sqlite3.connect(":memory:")`) — never point tests at `spendly.db`
- Use `pytest-flask`'s `client` fixture pattern — do not use `unittest.TestCase`
- Each test must be independent: set up its own data, tear down via the in-memory DB
- `compute_profile_stats(expenses)` must be a pure function — takes a list of `sqlite3.Row`-like dicts, returns a dict with keys `total_this_month`, `expense_count`, `top_category`
- Do not break the existing working route — the refactor must be transparent to the template

## Definition of done
- [ ] `pytest` exits with 0 failures
- [ ] `tests/conftest.py` exists with `app`, `client`, and `auth` fixtures
- [ ] `tests/test_profile.py` contains at least the following test cases:
  - `test_profile_redirects_when_logged_out` — `GET /profile` returns 302 → `/login`
  - `test_profile_renders_when_logged_in` — `GET /profile` returns 200 for an authenticated user
  - `test_profile_shows_correct_monthly_total` — total matches sum of current-month expenses only
  - `test_profile_shows_correct_expense_count` — count matches total expenses for the user
  - `test_profile_shows_top_category` — top category is the category with the highest cumulative amount
  - `test_profile_empty_state` — a user with no expenses sees the page without errors (no 500)
- [ ] `compute_profile_stats` is importable from `app` and tested directly (unit tests, no HTTP)
- [ ] Running `python app.py` still works — the refactor does not break the live route
