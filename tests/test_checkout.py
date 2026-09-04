import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage, CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage


class TestCheckout:

    def test_end_to_end_checkout_flow(self, page, app_url):
        # 1. Log in
        login_page = LoginPage(page)
        login_page.goto(app_url)
        login_page.login("standard_user", "secret_sauce")

        # 2. Add items to cart
        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        assert inventory_page.get_cart_count() == 2

        # 3. Go to cart and start checkout
        inventory_page.go_to_cart()
        cart_page = CartPage(page)
        assert cart_page.get_item_count() == 2
        cart_page.start_checkout()

        # 4. Fill in shipping info
        checkout_info_page = CheckoutInfoPage(page)
        checkout_info_page.fill_info("Shree", "QA", "30040")

        # 5. Review order and finish
        overview_page = CheckoutOverviewPage(page)
        assert "Total" in overview_page.get_total_text()
        overview_page.finish()

        # 6. Confirm completion
        complete_page = CheckoutCompletePage(page)
        confirmation = complete_page.get_confirmation_text()
        assert "Thank you" in confirmation, f"Unexpected confirmation text: {confirmation}"

    def test_checkout_requires_all_fields(self, page, app_url):
        login_page = LoginPage(page)
        login_page.goto(app_url)
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.go_to_cart()

        cart_page = CartPage(page)
        cart_page.start_checkout()

        # Leave postal code blank
        checkout_info_page = CheckoutInfoPage(page)
        checkout_info_page.fill_info("Shree", "QA", "")

        error = page.locator("[data-test='error']")
        assert error.is_visible(), "Expected a validation error for missing postal code"
