# Spec: Login and Logout

## Overview
This step wires up the login form that already exists in `templates/login.html` to a real `POST /login` route, and implements the `GET /logout` stub. When a user submits valid credentials, their `user_id` and `name` are stored in the Flask session and they are redirected to `/profile` (the next step's landing page). On invalid credentials the form re-renders with an inline error. Logout clears the session and redirects to `/login`. This step introduces Flask sessions as the authentication mechanism that all future protected routes will depend on.

## Depends on
- Step 1 — Database setup (`get_db` must be working)
- Step 2 — Registration (users must exist in the `users` table to log in against)

## Routes
- `GET /login` — render the blank login form — public
- `POST /login` — validate credentials, set session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/login` — public (currently a stub)

## Database changes
No new tables or columns. The existing `users` table has all required columns.

## Templates
- **Modify:** `templates/login.html`
  - Form markup and `{% if error %}` block already exist — no structural changes needed.
- **Modify:** `templates/base.html`
  - Navbar currently always shows "Sign in" and "Get started" links.
  - When a user is logged in (`session.user_id` is set), replace those links with the user's name and a "Sign out" link.

## Files to change
- `app.py` — add `secret_key`; convert `GET /login` stub to two-method route; add POST handler; implement `GET /logout`
- `templates/base.html` — make navbar session-aware

## Files to create
No new files.

## New dependencies
No new dependencies. `flask.session` is built into Flask. `werkzeug.security.check_password_hash` is already installed.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before sessions will work — use a hard-coded dev string (e.g. `"spendly-dev-secret"`) for now; a comment should note it must be replaced with an env var in production
- Store only `user_id` (int) and `name` (str) in the session — never store `password_hash`
- Invalid credentials (wrong email or wrong password) must show the same generic error: `"Invalid email or password"` — do not reveal which field is wrong
- Logout uses `session.clear()` then redirects to `/login`
- After successful login, redirect to `url_for('profile')`

## Definition of done
- [ ] `GET /login` renders the form without errors
- [ ] Submitting valid credentials (e.g. `demo@spendly.com` / `demo123`) sets the session and redirects to `/profile`
- [ ] Submitting an unknown email shows: `"Invalid email or password"` (no 500)
- [ ] Submitting a wrong password for a known email shows: `"Invalid email or password"` (no 500)
- [ ] `GET /logout` clears the session and redirects to `/login`
- [ ] After logout, visiting `/profile` does not show a logged-in state (full auth guard comes in Step 4)
- [ ] Navbar shows "Sign in" / "Get started" when logged out
- [ ] Navbar shows the user's name and a "Sign out" link when logged in
- [ ] `app.secret_key` is set and sessions persist across page loads
