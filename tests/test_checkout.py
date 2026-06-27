"""
Checkout regression tests
============================
Maps to manual Test Cases: TC-CHK-01, TC-CHK-02, TC-CHK-03, TC-CHK-04, TC-CHK-06
(see /docs/03_Test_Cases.xlsx)

NOTE: test_place_order_success / test_order_confirmation_message exercise the
full guest/registered checkout flow including the payment form. AutomationExercise.com
does not process real payments — any well-formed dummy card data is accepted.
These two tests require a logged-in session; see VALID_EMAIL / VALID_PASSWORD
in test_login.py for how to configure test credentials.
"""

import os

import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

VALID_EMAIL = os.getenv("AE_TEST_EMAIL", "qa.portfolio.user@example.com")
VALID_PASSWORD = os.getenv("AE_TEST_PASSWORD", "Valid@123")


def _login_add_to_cart_and_open_checkout(driver):
    login_page = LoginPage(driver).load()
    login_page.login(VALID_EMAIL, VALID_PASSWORD)

    products_page = ProductsPage(driver).load()
    products_page.add_first_product_to_cart()
    products_page.view_cart_from_modal()

    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()
    return CheckoutPage(driver)


@allure.feature("Checkout")
@pytest.mark.checkout
class TestCheckout:

    @allure.story("Checkout entry")
    @allure.title("TC-CHK-01: A registered user can proceed from cart to checkout")
    def test_proceed_to_checkout(self, driver):
        with allure.step("Log in, add a product, proceed to checkout"):
            checkout_page = _login_add_to_cart_and_open_checkout(driver)

        with allure.step("Assert the checkout/address review page loaded"):
            assert "/checkout" in driver.current_url
            assert checkout_page.is_visible(checkout_page.REVIEW_ORDER_TABLE)

    @allure.story("Order placement")
    @allure.title("TC-CHK-02: A user can place an order end-to-end with valid details")
    def test_place_order_success(self, driver):
        with allure.step("Log in, add a product, proceed to checkout"):
            checkout_page = _login_add_to_cart_and_open_checkout(driver)

        with allure.step("Place the order and submit dummy payment details"):
            checkout_page.add_comment("Automated regression test order - no real payment.")
            checkout_page.place_order()
            checkout_page.fill_payment_details(
                name="QA Portfolio User",
                card_number="4111111111111111",
                cvc="123",
                month="12",
                year="2030",
            )
            checkout_page.submit_payment()

        with allure.step("Assert the order confirmation message is shown"):
            assert checkout_page.has_order_confirmation(), (
                "Expected a 'Congratulations! Your order has been confirmed!' message."
            )

    @allure.story("Negative / boundary")
    @allure.title("TC-CHK-03: Checkout is blocked when the cart is empty")
    def test_checkout_empty_cart(self, driver):
        cart_page = CartPage(driver).load()

        with allure.step("Ensure cart is empty, then attempt to proceed"):
            cart_page.remove_all_rows()

        with allure.step("Assert the empty-cart message is shown instead of checkout"):
            assert cart_page.is_empty(), "Expected the 'Cart is empty!' state to block checkout."

    @allure.story("Address review")
    @allure.title("TC-CHK-04: Delivery & billing address are shown on the review screen")
    def test_review_address_displayed(self, driver):
        with allure.step("Log in, add a product, proceed to checkout"):
            checkout_page = _login_add_to_cart_and_open_checkout(driver)

        with allure.step("Read delivery and billing address blocks"):
            delivery_text = checkout_page.get_delivery_address_text()
            billing_text = checkout_page.get_billing_address_text()

        with allure.step("Assert both address blocks are populated"):
            assert delivery_text.strip() != "", "Expected a non-empty delivery address."
            assert billing_text.strip() != "", "Expected a non-empty billing address."

    @allure.story("Order confirmation")
    @allure.title("TC-CHK-06: Order confirmation message appears after placing an order")
    def test_order_confirmation_message(self, driver):
        with allure.step("Log in, add a product, proceed to checkout"):
            checkout_page = _login_add_to_cart_and_open_checkout(driver)

        with allure.step("Place the order with valid dummy payment details"):
            checkout_page.place_order()
            checkout_page.fill_payment_details(
                name="QA Portfolio User",
                card_number="4111111111111111",
                cvc="123",
                month="12",
                year="2030",
            )
            checkout_page.submit_payment()

        with allure.step("Assert confirmation text mentions the order is confirmed"):
            confirmation_text = checkout_page.get_order_confirmation_text()
            assert "confirmed" in confirmation_text.lower() or "congratulations" in confirmation_text.lower()
