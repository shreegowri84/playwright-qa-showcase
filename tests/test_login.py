import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestLogin:

    def test_successful_login(self, page, app_url):
        login_page = LoginPage(page)
        login_page.goto(app_url)
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(page)
        assert inventory_page.is_loaded(), "Expected to land on the Products page after login"

    @pytest.mark.parametrize(
        "username, password, expected_error_fragment",
        [
            ("locked_out_user", "secret_sauce", "locked out"),
            ("standard_user", "wrong_password", "do not match"),
            ("", "secret_sauce", "Username is required"),
            ("standard_user", "", "Password is required"),
        ],
        ids=["locked-out-user", "wrong-password", "missing-username", "missing-password"],
    )
    def test_login_failure_scenarios(
        self, page, app_url, username, password, expected_error_fragment
    ):
        login_page = LoginPage(page)
        login_page.goto(app_url)
        login_page.login(username, password)

        assert login_page.is_error_visible(), "Expected an error message to be shown"
        error_text = login_page.get_error_text()
        assert expected_error_fragment.lower() in error_text.lower(), (
            f"Expected error to mention '{expected_error_fragment}', got: '{error_text}'"
        )
