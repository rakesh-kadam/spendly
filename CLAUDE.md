# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
python app.py        # starts on http://localhost:5001 (debug mode on)
```

Dependencies are pinned in `requirements.txt`. Install with:

```bash
pip3 install -r requirements.txt
```

## Running tests

```bash
pytest               # run all tests
pytest tests/test_foo.py::test_bar   # run a single test
```

Test runner is `pytest` + `pytest-flask`. No test files exist yet — students add them as features are built.

## Architecture

This is a **Flask + SQLite** app with no ORM. All routes live in `app.py`; database helpers will live in `database/db.py` (not yet implemented — see the stub comments there).

**Request flow:**
```
browser → app.py route → render_template() → templates/*.html
                        ↘ database/db.py (get_db / init_db / seed_db)
```

**Templates** extend `base.html`, which provides the navbar, footer, and asset links. Page-specific JS goes in `{% block scripts %}` at the bottom of individual templates (see `landing.html` for the video modal example). Global JS goes in `static/js/main.js`.

**Styles** all live in `static/css/style.css` — there is no separate per-page stylesheet. The file is organized into labeled sections (Variables, Reset, Navbar, Hero, Buttons, etc.).

## Placeholder routes

Several routes in `app.py` are stubs that students implement step by step:

| Route | Step |
|---|---|
| `GET /logout` | Step 3 |
| `GET /profile` | Step 4 |
| `GET /expenses/add` | Step 7 |
| `GET/POST /expenses/<id>/edit` | Step 8 |
| `GET /expenses/<id>/delete` | Step 9 |

`database/db.py` is also a stub — `get_db()`, `init_db()`, and `seed_db()` need to be written in Step 1.

## Git commit style

Use single quotes for commit messages in the terminal (double quotes cause a shell parse error in this environment):

```bash
git commit -m 'your message here'
```
