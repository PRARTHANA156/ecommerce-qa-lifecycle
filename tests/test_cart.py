"""
Cart regression tests
=======================
Maps to manual Test Cases: TC-CRT-01, TC-CRT-02, TC-CRT-03, TC-CRT-06, TC-CRT-07
(see /docs/03_Test_Cases.xlsx)
"""

import allure
import pytest

from pages.cart_page import CartPage
from pages.products_page import ProductsPage


@allure.feature("Cart")
@pytest.mark.cart
class TestCart:

    @allure.story("Add to cart")
    @allure.title("TC-CRT-01: A single product can be added to the cart")
    def test_add_single_product_to_cart(self, driver):
        products_page = ProductsPage(driver).load()
        cart_page = CartPage(driver)

        with allure.step("Add the first product to the cart and open the cart"):
            products_page.add_first_product_to_cart()
            products_page.view_cart_from_modal()

        with allure.step("Assert exactly one line item is present"):
            assert cart_page.get_line_item_count() == 1, (
                "Expected exactly one line item after adding a single product."
            )

    @allure.story("Add to cart")
    @allure.title("TC-CRT-02: Multiple distinct products can be added to the cart")
    def test_add_multiple_products_to_cart(self, driver):
        products_page = ProductsPage(driver).load()
        cart_page = CartPage(driver)

        with allure.step("Add the first and second products to the cart"):
            products_page.add_nth_product_to_cart(0)
            products_page.continue_shopping()
            products_page.add_nth_product_to_cart(1)
            products_page.view_cart_from_modal()

        with allure.step("Assert two distinct line items are present"):
            assert cart_page.get_line_item_count() == 2, (
                "Expected two distinct line items after adding two products."
            )

    @allure.story("Quantity & subtotal")
    @allure.title("TC-CRT-03: Increasing quantity recalculates the line subtotal")
    def test_increase_quantity_updates_subtotal(self, driver):
        products_page = ProductsPage(driver).load()
        cart_page = CartPage(driver)

        with allure.step("Add a product to the cart"):
            products_page.add_first_product_to_cart()
            products_page.view_cart_from_modal()

        with allure.step("Read unit price and line total for the single item"):
            unit_price = cart_page.get_price_for_row(0)
            quantity = cart_page.get_quantity_for_row(0)
            line_total = cart_page.get_total_for_row(0)

        with allure.step("Assert subtotal == unit price * quantity"):
            assert round(unit_price * quantity, 2) == round(line_total, 2), (
                f"Expected subtotal {unit_price * quantity}, got {line_total}."
            )

    @allure.story("Remove items")
    @allure.title("TC-CRT-06: A single item can be removed from the cart")
    def test_remove_single_item(self, driver):
        products_page = ProductsPage(driver).load()
        cart_page = CartPage(driver)

        with allure.step("Add two products, then remove one"):
            products_page.add_nth_product_to_cart(0)
            products_page.continue_shopping()
            products_page.add_nth_product_to_cart(1)
            products_page.view_cart_from_modal()
            initial_count = cart_page.get_line_item_count()
            cart_page.remove_row(0)

        with allure.step("Assert the line-item count decreased by exactly one"):
            assert cart_page.get_line_item_count() == initial_count - 1

    @allure.story("Remove items")
    @allure.title("TC-CRT-07: Removing all items shows the empty-cart state")
    def test_remove_all_items_empty_cart(self, driver):
        products_page = ProductsPage(driver).load()
        cart_page = CartPage(driver)

        with allure.step("Add a product, then remove every item"):
            products_page.add_first_product_to_cart()
            products_page.view_cart_from_modal()
            cart_page.remove_all_rows()

        with allure.step("Assert the empty-cart message is displayed"):
            assert cart_page.is_empty(), "Expected the 'Cart is empty!' message."
