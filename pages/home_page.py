"""HomePage — header / global navigation Page Object."""

from selenium.webdriver.common.by import By

from .base_page import BasePage

BASE_URL = "https://automationexercise.com"


class HomePage(BasePage):
    URL = BASE_URL + "/"

    # Header / nav locators
    LOGO = (By.CSS_SELECTOR, "div.logo a img")
    NAV_PRODUCTS = (By.CSS_SELECTOR, "a[href='/products']")
    NAV_CART = (By.CSS_SELECTOR, "a[href='/view_cart']")
    NAV_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")
    NAV_LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")
    LOGGED_IN_AS = (By.XPATH, "//a[contains(text(),'Logged in as')]")

    def load(self):
        self.open(self.URL)
        return self

    def go_to_login(self):
        self.click(self.NAV_LOGIN)
        return self

    def go_to_products(self):
        self.click(self.NAV_PRODUCTS)
        return self

    def go_to_cart(self):
        self.click(self.NAV_CART)
        return self

    def logout(self):
        self.click(self.NAV_LOGOUT)
        return self

    def is_logged_in(self):
        return self.is_visible(self.LOGGED_IN_AS, timeout=5)

    def is_logged_out_state(self):
        return self.is_visible(self.NAV_LOGIN, timeout=5)
