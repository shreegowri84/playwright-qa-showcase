"""Page Object for the cart and checkout flow."""


class CartPage:
    def __init__(self, page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("#checkout")

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def start_checkout(self):
        self.checkout_button.click()


class CheckoutInfoPage:
    def __init__(self, page):
        self.page = page
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.postal_code = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()


class CheckoutOverviewPage:
    def __init__(self, page):
        self.page = page
        self.finish_button = page.locator("#finish")
        self.total_label = page.locator(".summary_total_label")

    def get_total_text(self) -> str:
        return self.total_label.inner_text()

    def finish(self):
        self.finish_button.click()


class CheckoutCompletePage:
    def __init__(self, page):
        self.page = page
        self.complete_header = page.locator(".complete-header")

    def get_confirmation_text(self) -> str:
        return self.complete_header.inner_text()
