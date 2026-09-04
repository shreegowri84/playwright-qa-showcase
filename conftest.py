"""
Shared pytest fixtures for the suite.

- `page` fixture is provided by pytest-playwright out of the box, but we
  extend behavior here via a hook that captures a screenshot whenever a
  test fails, saved to ./screenshots/<test_name>.png
"""
import os
import pytest

SCREENSHOT_DIR = "screenshots"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Set a consistent viewport for all tests so layouts are reproducible."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
    }


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    After each test phase, check if it failed. If it did and a Playwright
    `page` fixture was in use, save a screenshot for debugging.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            safe_name = item.name.replace("/", "_")
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
            try:
                page.screenshot(path=screenshot_path)
                print(f"\nScreenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"\nCould not capture screenshot: {e}")


@pytest.fixture
def app_url():
    return "https://www.saucedemo.com"
