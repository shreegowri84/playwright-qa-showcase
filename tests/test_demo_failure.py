"""
This file contains ONE intentionally failing test.

It exists purely to demonstrate that the reporting pipeline (screenshots,
HTML report, Allure dashboard) correctly surfaces failures, not just passes.
Delete this file once you've taken your screenshot, or keep it if you want
your CI badge to stay visibly "real" rather than suspiciously perfect.
"""
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestDemoFailure:

    def test_demo_intentional_failure(self, page, app_url):
        """
        Intentionally asserts something false to produce a failing test.
        Also exercises the screenshot-on-failure hook in conftest.py.
        """
        login_page = LoginPage(page)
        login_page.goto(app_url)
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(page)
        assert inventory_page.get_cart_count() == 99, (
            "Intentional failure for demo purposes: cart is empty on login, "
            "not 99. This test is meant to fail — see module docstring."
        )