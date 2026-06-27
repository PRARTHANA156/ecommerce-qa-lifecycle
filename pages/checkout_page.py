"""CheckoutPage — address review, order placement, payment & confirmation."""

from selenium.webdriver.common.by import By

from .base_page import BasePage

BASE_URL = "https://automationexercise.com"


class CheckoutPage(BasePage):
    URL = BASE_URL + "/checkout"

    DELIVERY_ADDRESS_BLOCK = (By.CSS_SELECTOR, "ul#address_delivery")
    BILLING_ADDRESS_BLOCK = (By.CSS_SELECTOR, "ul#address_invoice")
    REVIEW_ORDER_TABLE = (By.CSS_SELECTOR, "table.table-condensed")
    ORDER_COMMENT_BOX = (By.CSS_SELECTOR, "textarea[name='message']")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "a.check_out")

    # Payment page
    NAME_ON_CARD = (By.NAME, "name_on_card")
    CARD_NUMBER = (By.NAME, "card_number")
    CVC = (By.NAME, "cvc")
    EXPIRY_MONTH = (By.NAME, "expiry_month")
    EXPIRY_YEAR = (By.NAME, "expiry_year")
    PAY_BUTTON = (By.ID, "submitOrder")

    ORDER_SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(),'Congratulations')]")

    def load(self):
        self.open(self.URL)
        return self

    def get_delivery_address_text(self):
        return self.get_text(self.DELIVERY_ADDRESS_BLOCK)

    def get_billing_address_text(self):
        return self.get_text(self.BILLING_ADDRESS_BLOCK)

    def add_comment(self, comment):
        self.type_text(self.ORDER_COMMENT_BOX, comment)
        return self

    def place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)
        return self

    def fill_payment_details(self, name, card_number, cvc, month, year):
        self.type_text(self.NAME_ON_CARD, name)
        self.type_text(self.CARD_NUMBER, card_number)
        self.type_text(self.CVC, cvc)
        self.type_text(self.EXPIRY_MONTH, month)
        self.type_text(self.EXPIRY_YEAR, year)
        return self

    def submit_payment(self):
        self.click(self.PAY_BUTTON)
        return self

    def get_order_confirmation_text(self):
        return self.get_text(self.ORDER_SUCCESS_MESSAGE, timeout=20)

    def has_order_confirmation(self):
        return self.is_visible(self.ORDER_SUCCESS_MESSAGE, timeout=20)
