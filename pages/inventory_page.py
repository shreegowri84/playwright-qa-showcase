"""Page Object for the Sauce Demo product listing (inventory) page."""


class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.inventory_list = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.page_title = page.locator(".title")
        self.sort_dropdown = page.locator(".product_sort_container")

    def is_loaded(self) -> bool:
        return self.page_title.inner_text() == "Products"

    def add_item_to_cart_by_name(self, item_name: str):
        item = self.page.locator(".inventory_item").filter(has_text=item_name)
        item.locator("button", has_text="Add to cart").click()

    def remove_item_from_cart_by_name(self, item_name: str):
        item = self.page.locator(".inventory_item").filter(has_text=item_name)
        item.locator("button", has_text="Remove").click()

    def get_cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def go_to_cart(self):
        self.cart_link.click()

    def sort_by(self, option_value: str):
        """option_value examples: 'lohi', 'hilo', 'az', 'za'"""
        self.sort_dropdown.select_option(option_value)

    def get_item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()
