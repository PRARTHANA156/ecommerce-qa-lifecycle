"""
Login regression tests
=======================
Maps to manual Test Cases: TC-LOG-01, TC-LOG-02, TC-LOG-04, TC-LOG-05, TC-LOG-08
(see /docs/03_Test_Cases.xlsx)

NOTE: These tests run against the public AutomationExercise.com demo site.
`VALID_EMAIL` / `VALID_PASSWORD` must correspond to an account you have
already registered on that site (sign up once via the UI or the
`createAccount` API, then update the constants below or set them via
environment variables).
"""

import os

import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage

VALID_EMAIL = os.getenv("AE_TEST_EMAIL", "qa.portfolio.user@example.com")
VALID_PASSWORD = os.getenv("AE_TEST_PASSWORD", "Valid@123")


@allure.feature("Login")
@pytest.mark.login
class TestLogin:

    @allure.story("Valid credentials")
    @allure.title("TC-LOG-01: User can log in with valid email & password")
    def test_valid_login(self, driver):
        login_page = LoginPage(driver).load()
        home_page = HomePage(driver)

        with allure.step("Submit valid credentials"):
            login_page.login(VALID_EMAIL, VALID_PASSWORD)

        with allure.step("Assert the user lands in a logged-in state"):
            assert home_page.is_logged_in(), (
                "Expected 'Logged in as <user>' in the header after a valid login."
            )

    @allure.story("Invalid credentials")
    @allure.title("TC-LOG-02: Login is rejected for a valid email + wrong password")
    def test_login_invalid_password(self, driver):
        login_page = LoginPage(driver).load()

        with allure.step("Submit a valid email with an incorrect password"):
            login_page.login(VALID_EMAIL, "WrongPass1")

        with allure.step("Assert an inline error message is shown"):
            assert login_page.has_login_error(), (
                "Expected an 'incorrect' credentials error message."
            )

    @allure.story("Field validation")
    @allure.title("TC-LOG-04: Login is blocked when the email field is empty")
    def test_login_empty_email(self, driver):
        login_page = LoginPage(driver).load()

        with allure.step("Leave email blank, fill password, submit"):
            login_page.type_text(login_page.LOGIN_PASSWORD, VALID_PASSWORD)
            login_page.click(login_page.LOGIN_BUTTON)

        with allure.step("Assert the form did not navigate away (still on /login)"):
            assert "/login" in driver.current_url, (
                "Expected the required-field validation to block submission."
            )

    @allure.story("Field validation")
    @allure.title("TC-LOG-05: Login is blocked when the password field is empty")
    def test_login_empty_password(self, driver):
        login_page = LoginPage(driver).load()

        with allure.step("Fill email, leave password blank, submit"):
            login_page.type_text(login_page.LOGIN_EMAIL, VALID_EMAIL)
            login_page.click(login_page.LOGIN_BUTTON)

        with allure.step("Assert the form did not navigate away (still on /login)"):
            assert "/login" in driver.current_url, (
                "Expected the required-field validation to block submission."
            )

    @allure.story("Logout")
    @allure.title("TC-LOG-08: A logged-in user can log out successfully")
    def test_logout_after_login(self, driver):
        login_page = LoginPage(driver).load()
        home_page = HomePage(driver)

        with allure.step("Log in with valid credentials"):
            login_page.login(VALID_EMAIL, VALID_PASSWORD)
            assert home_page.is_logged_in(), "Pre-condition failed: could not log in."

        with allure.step("Click Logout"):
            home_page.logout()

        with allure.step("Assert the user is returned to a logged-out state"):
            assert home_page.is_logged_out_state(), (
                "Expected the 'Signup / Login' link to reappear after logout."
            )
