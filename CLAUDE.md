# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Spendly** — a Flask + SQLite expense tracker built as a step-by-step course project (CampusX). Many pieces are intentionally stubbed and get implemented in numbered "Steps"; comments like `coming in Step 7` mark where each feature lands. Amounts are in rupees (₹).

## Commands

A virtualenv lives at `venv/` (Windows layout).

```bash
# Install deps
venv/Scripts/pip install -r requirements.txt

# Run the dev server (debug mode, http://localhost:5001 — note: not Flask's default 5000)
venv/Scripts/python app.py

# Tests (pytest + pytest-flask are in requirements; no tests/ directory exists yet)
venv/Scripts/python -m pytest
venv/Scripts/python -m pytest tests/test_file.py::test_name   # single test
```

There is no linter, formatter, or build step configured.

## Architecture

- **`app.py`** — the single Flask app module; all routes live here (no blueprints, no app factory). Public pages (`/`, `/login`, `/register`, `/terms`, `/privacy`) render templates. Placeholder routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) return strings until their step is implemented — keep their endpoint names stable since templates link to them via `url_for`.
- **`database/db.py`** — currently empty by design (Step 1). It is expected to expose `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (`CREATE TABLE IF NOT EXISTS` for all tables), and `seed_db()` (dev sample data). The DB file `expense_tracker.db` is gitignored.
- **Templates** — every page extends `templates/base.html`, which provides the navbar, footer, and the blocks `title`, `head` (page-specific CSS), `content`, and `scripts` (page-specific JS). `login.html`/`register.html` already contain POST forms and render an optional `error` variable, so the handlers should pass `error=` on failure.
- **Static assets** — `static/css/style.css` holds global styles and the design tokens (CSS custom properties in `:root`: `--ink*`, `--paper*`, `--accent*`, `--danger`, `--radius-*`, fonts DM Serif Display / DM Sans). Use these variables rather than hard-coded colors. Page-specific styles go in their own file (e.g. `landing.css`, loaded via the `head` block). Small page-specific scripts are inline in the `scripts` block (e.g. the YouTube modal in `landing.html`); `static/js/main.js` is the shared script, currently empty.

## Conventions

- Commit messages use a `area: description` prefix (e.g. `landing: add privacy policy page and route`).
