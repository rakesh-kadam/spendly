# Spec: Registration

## Overview
This step wires up the registration form that already exists in `templates/register.html` to a real `POST /register` route. When a new visitor submits the form, their name, email, and password are validated, the password is hashed, and the record is inserted into the `users` table. On success the user is redirected to `/login`; on failure the form re-renders with a descriptive error message. This is the first step that writes user-generated data to the database and gates all future authenticated features.

## Depends on
- Step 1 — Database setup (`get_db`, `init_db`, `seed_db` must be working)

## Routes
- `GET /register` — render the blank registration form — public
- `POST /register` — validate form data, insert user, redirect to `/login` — public

## Database changes
No new tables or columns. The `users` table created in Step 1 already has all required columns:
- `name TEXT NOT NULL`
- `email TEXT UNIQUE NOT NULL`
- `password_hash TEXT NOT NULL`
- `created_at TEXT DEFAULT (datetime('now'))`

## Templates
- **Modify:** `templates/register.html`
  - The form markup already exists and is correct.
  - Ensure `{{ error }}` block is present and styled (already in template — no change needed if it renders).
  - No structural changes required unless the error block needs a CSS class fix.

## Files to change
- `app.py` — convert `GET /register` stub to a two-method route; add POST handler logic

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug.security` (already installed) provides `generate_password_hash`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Server-side validation must check:
  - `name` is non-empty
  - `email` is non-empty and contains `@`
  - `password` is at least 8 characters
- Duplicate email must be caught (SQLite UNIQUE constraint) and shown as a friendly error, not a 500
- After successful registration, redirect to `/login` with `302`
- Do not log the user in automatically — login is a separate step (Step 3)
- Import `redirect`, `url_for`, `request` from `flask` as needed

## Definition of done
- [ ] `GET /register` still renders the form without errors
- [ ] Submitting the form with valid data inserts a new row in `users` and redirects to `/login`
- [ ] Password is stored as a hash (not plaintext) — verify in `spendly.db` with a DB browser or query
- [ ] Submitting with an already-registered email shows an inline error: "An account with that email already exists"
- [ ] Submitting with a password shorter than 8 characters shows an inline error: "Password must be at least 8 characters"
- [ ] Submitting with an empty name or email shows an appropriate inline error
- [ ] No 500 errors under any of the above invalid-input scenarios
- [ ] Redirect after success lands on `/login`
