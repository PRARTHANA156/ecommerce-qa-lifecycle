"""CartPage — line items, quantity updates, removal, totals."""

from selenium.webdriver.common.by import By

from .base_page import BasePage

BASE_URL = "https://automationexercise.com"


class CartPage(BasePage):
    URL = BASE_URL + "/view_cart"

    CART_ROWS = (By.CSS_SELECTOR, "tr[id^='product-']")
    EMPTY_CART_MESSAGE = (By.XPATH, "//b[contains(text(),'Cart is empty')]")
    CONTINUE_SHOPPING_LINK = (By.XPATH, "//a[contains(@href,'/products') and contains(text(),'here')]")

    PROCEED_TO_CHECKOUT_BUTTON = (By.CSS_SELECTOR, "a.check_out")

    def load(self):
        self.open(self.URL)
        return self

    def get_line_item_count(self):
        return len(self.driver.find_elements(*self.CART_ROWS))

    def is_empty(self):
        return self.is_visible(self.EMPTY_CART_MESSAGE, timeout=8)

    def get_quantity_for_row(self, index=0):
        rows = self.find_all(self.CART_ROWS)
        qty_el = rows[index].find_element(By.CSS_SELECTOR, "td.cart_quantity button")
        return int(qty_el.text.strip())

    def get_price_for_row(self, index=0):
        rows = self.find_all(self.CART_ROWS)
        price_text = rows[index].find_element(By.CSS_SELECTOR, "td.cart_price p").text
        return float(price_text.replace("Rs.", "").replace(",", "").strip())

    def get_total_for_row(self, index=0):
        rows = self.find_all(self.CART_ROWS)
        total_text = rows[index].find_element(By.CSS_SELECTOR, "td.cart_total p").text
        return float(total_text.replace("Rs.", "").replace(",", "").strip())

    def remove_row(self, index=0):
        rows = self.find_all(self.CART_ROWS)
        delete_link = rows[index].find_element(By.CSS_SELECTOR, "td.cart_delete a.cart_quantity_delete")
        self.driver.execute_script("arguments[0].click();", delete_link)
        return self

    def remove_all_rows(self):
        while self.get_line_item_count() > 0:
            self.remove_row(0)
        return self

    def proceed_to_checkout(self):
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)
        return self
