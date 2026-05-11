# Spec: Profile Page Design

## Overview
This step implements the `GET /profile` route and its template, replacing the current placeholder string. The profile page is the authenticated home screen for Spendly — it shows the logged-in user's name, a summary of their spending (total this month, number of expenses, top category), and a list of their recent expenses. It also acts as the first protected route: any unauthenticated visitor is redirected to `/login`. This is the centrepiece of the app that all subsequent CRUD steps will link back to.

## Depends on
- Step 1 — Database setup (`get_db` must be working; `expenses` table must exist with seed data)
- Step 2 — Registration (users must exist in the `users` table)
- Step 3 — Login and Logout (session must carry `user_id` and `name`)

## Routes
- `GET /profile` — render the authenticated profile/dashboard page — **logged-in only** (redirect to `/login` if not authenticated)

## Database changes
No database changes. The `users` and `expenses` tables created in Step 1 already contain all required columns.

## Templates
- **Create:** `templates/profile.html` — full profile/dashboard page extending `base.html`
  - Greeting header with the user's name
  - Summary strip: total spent this month, expense count, top spending category
  - Table or card list of all expenses (amount, category, date, description) ordered by date descending
  - "Add expense" call-to-action button (links to `/expenses/add` — placeholder until Step 7)
- **Modify:** none

## Files to change
- `app.py` — replace the `GET /profile` stub string with a real route that:
  1. Checks `session.get("user_id")`; if missing, `redirect(url_for("login"))`
  2. Queries all expenses for the logged-in user
  3. Computes summary stats (total this month, count, top category) in Python
  4. Passes data to `render_template("profile.html", ...)`

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with werkzeug (no new password logic here, but do not break existing auth)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Auth guard: `if not session.get("user_id"): return redirect(url_for("login"))` at the top of the route
- Stats must be computed in Python from the query results — do not use SQL aggregation for display values (keep it simple and readable for students)
- "This month" means the current calendar month (`datetime.now().strftime("%Y-%m")` prefix match on `date` column)
- Top category is the category with the highest total amount for the current user (all-time is fine if no expenses this month)
- If the user has no expenses, show a friendly empty state rather than an error
- The "Add expense" button must be present but may link to the placeholder route `/expenses/add`

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in renders the profile page without errors
- [ ] The page displays the logged-in user's name
- [ ] Total spent this month is shown and matches the sum of the demo user's May 2026 expenses (`319.55`)
- [ ] Expense count is shown and matches the demo data (`8` expenses)
- [ ] Top spending category is shown (should be `Bills` for the demo data based on highest single amount, or computed correctly)
- [ ] All 8 seed expenses are listed, ordered by date descending
- [ ] An "Add expense" button or link is visible on the page
- [ ] No 500 errors for the demo user or a freshly registered user with no expenses
- [ ] Navbar shows the user's name and "Sign out" link (inherited from `base.html`)
