# Playwright QA Showcase — Page Object Model + pytest

A small, production-style UI test automation framework built with **Playwright + Python + pytest**, demonstrating the Page Object Model (POM) pattern, fixtures, parametrization, and CI integration via GitHub Actions.

Target app: [saucedemo.com](https://www.saucedemo.com) — a public site built for QA practice.

## Why this project exists

Most "Playwright hello world" repos are a single script. This one is structured the way a real test suite should be:

- **Separation of concerns** — pages know how to interact with the UI; tests know what to assert
- **Reusable fixtures** — browser/page setup lives in one place (`conftest.py`)
- **Data-driven tests** — parametrized login scenarios instead of copy-pasted test functions
- **CI-ready** — GitHub Actions workflow runs the suite headlessly on every push
- **Failure artifacts** — screenshots auto-captured on test failure for debugging

## Project structure

```
playwright-qa-showcase/
├── pages/
│   ├── login_page.py       # Page Object for the login screen
│   ├── inventory_page.py   # Page Object for the product listing
│   └── cart_page.py        # Page Object for the cart
├── tests/
│   ├── test_login.py       # Positive + negative login scenarios (parametrized)
│   ├── test_cart.py        # Add/remove items from cart
│   └── test_checkout.py    # End-to-end checkout flow
├── conftest.py              # Shared pytest fixtures (browser, page, screenshot-on-fail)
├── pytest.ini                # pytest configuration
├── requirements.txt
├── .github/workflows/tests.yml   # CI pipeline
└── .gitignore
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install --with-deps chromium
```

## Running the tests

```bash
# Run the full suite headlessly
pytest

# Run with a visible browser
pytest --headed

# Run a specific file
pytest tests/test_login.py -v

# Run in parallel (requires pytest-xdist, included in requirements.txt)
pytest -n auto
```

Screenshots for any failed test are saved to `screenshots/`.

## Test reports

Every run generates two report formats automatically (configured in `pytest.ini`):

**HTML report (self-contained, single file — good for a quick screenshot or email)**
```bash
pytest
open reports/report.html      # macOS; use `start` on Windows, `xdg-open` on Linux
```

**Allure report (interactive dashboard — trend graphs, categorized failures, timeline, retries)**

Allure needs the [Allure commandline tool](https://allurereport.org/docs/install/) installed separately (it's not a Python package):

```bash
# macOS
brew install allure

# Windows (scoop)
scoop install allure

# Or via npm (any OS)
npm install -g allure-commandline
```

Then:
```bash
pytest                          # writes raw results to allure-results/
allure serve allure-results     # builds + opens the report in your browser
```

`allure serve` is the fastest way to view it locally. For a static file to share, use `allure generate allure-results -o allure-report --clean` instead.

**In CI:** the GitHub Actions workflow uploads the HTML report as a build artifact on every run, and publishes the Allure report to GitHub Pages automatically on pushes to `main` (with history preserved across runs — so you get pass/fail trend graphs over time). Enable GitHub Pages in the repo settings (source: `gh-pages` branch) for this to work.

## What's demonstrated here

| Concept | Where |
|---|---|
| Page Object Model | `pages/*.py` |
| Fixture-based setup/teardown | `conftest.py` |
| Parametrized (data-driven) tests | `tests/test_login.py` |
| Explicit waits / auto-waiting assertions | throughout `pages/*.py` |
| Failure screenshot hook | `conftest.py` |
| CI pipeline | `.github/workflows/tests.yml` |
| HTML + Allure reporting | `pytest.ini`, CI pipeline |

## Extending this

Natural next steps if you fork this: add API-level setup (skip the UI login and seed state via requests), visual regression checks, or wire it into Allure/HTML reporting.

---

Built as a portfolio/teaching example. Feedback and PRs welcome.
