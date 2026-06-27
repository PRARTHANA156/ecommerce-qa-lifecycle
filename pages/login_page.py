"""LoginPage — covers both the 'Login to your account' and
'New User Signup!' forms that live on the /login route."""

from selenium.webdriver.common.by import By

from .base_page import BasePage

BASE_URL = "https://automationexercise.com"


class LoginPage(BasePage):
    URL = BASE_URL + "/login"

    # Login form
    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR = (By.XPATH, "//p[contains(text(),'incorrect')]")

    # Signup form
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
    SIGNUP_ERROR = (By.XPATH, "//p[contains(text(),'already exist')]")

    def load(self):
        self.open(self.URL)
        return self

    # --- Login -----------------------------------------------------------
    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_login_error_text(self):
        return self.get_text(self.LOGIN_ERROR, timeout=8)

    def has_login_error(self):
        return self.is_visible(self.LOGIN_ERROR, timeout=8)

    def is_login_email_required(self):
        """True if the browser-native 'required' validation blocks submission."""
        element = self.find(self.LOGIN_EMAIL)
        return element.get_attribute("validationMessage") != "" or not element.get_attribute("value")

    # --- Signup ------------------------------------------------------------
    def start_signup(self, name, email):
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)
        return self
