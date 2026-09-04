import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.fixture
def logged_in_inventory_page(page, app_url):
    """Reusable fixture: log in and land on the inventory page."""
    login_page = LoginPage(page)
    login_page.goto(app_url)
    login_page.login("standard_user", "secret_sauce")
    return InventoryPage(page)


class TestCart:

    def test_add_single_item_updates_badge(self, logged_in_inventory_page):
        inventory_page = logged_in_inventory_page
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        assert inventory_page.get_cart_count() == 1

    def test_add_multiple_items_updates_badge(self, logged_in_inventory_page):
        inventory_page = logged_in_inventory_page
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bolt T-Shirt")
        assert inventory_page.get_cart_count() == 3

    def test_remove_item_updates_badge(self, logged_in_inventory_page):
        inventory_page = logged_in_inventory_page
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        inventory_page.remove_item_from_cart_by_name("Sauce Labs Backpack")
        assert inventory_page.get_cart_count() == 1

    def test_cart_reflects_items_added_on_inventory(self, page, logged_in_inventory_page):
        inventory_page = logged_in_inventory_page
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Fleece Jacket")
        inventory_page.go_to_cart()

        cart_page = CartPage(page)
        cart_items = cart_page.get_item_names()
        assert set(cart_items) == {"Sauce Labs Backpack", "Sauce Labs Fleece Jacket"}

    @pytest.mark.parametrize(
        "sort_option, expect_ascending",
        [("lohi", True), ("hilo", False)],
        ids=["price-low-to-high", "price-high-to-low"],
    )
    def test_sort_by_price(self, page, logged_in_inventory_page, sort_option, expect_ascending):
        inventory_page = logged_in_inventory_page
        inventory_page.sort_by(sort_option)

        prices = page.locator(".inventory_item_price").all_inner_texts()
        numeric_prices = [float(p.replace("$", "")) for p in prices]

        expected = sorted(numeric_prices, reverse=not expect_ascending)
        assert numeric_prices == expected, f"Items were not sorted correctly by {sort_option}"
