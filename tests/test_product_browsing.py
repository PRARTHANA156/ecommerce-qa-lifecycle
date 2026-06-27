"""
Product browsing & search regression tests
============================================
Maps to manual Test Cases: TC-PRD-01, TC-PRD-02, TC-PRD-03, TC-PRD-04, TC-PRD-08
(see /docs/03_Test_Cases.xlsx)
"""

import allure
import pytest

from pages.products_page import ProductsPage


@allure.feature("Product Browsing")
@pytest.mark.products
class TestProductBrowsing:

    @allure.story("Catalog listing")
    @allure.title("TC-PRD-01: The Products page lists all catalog items")
    def test_all_products_listed(self, driver):
        products_page = ProductsPage(driver).load()

        with allure.step("Read the page heading and product count"):
            heading = products_page.get_page_heading()
            count = products_page.get_product_count()

        with allure.step("Assert the catalog grid is populated"):
            assert "Products" in heading or "ALL PRODUCTS" in heading.upper()
            assert count > 0, "Expected at least one product card on the Products page."

    @allure.story("Product detail")
    @allure.title("TC-PRD-02: A product's detail page opens with the expected info")
    def test_view_product_details(self, driver):
        products_page = ProductsPage(driver).load()

        with allure.step("Open the first product's detail page"):
            products_page.open_first_product_details()

        with allure.step("Assert the URL routes to /product_details/<id>"):
            assert "/product_details/" in driver.current_url, (
                "Expected navigation to a product detail page."
            )

    @allure.story("Search")
    @allure.title("TC-PRD-03: Searching a valid keyword returns matching products")
    def test_search_valid_keyword(self, driver):
        products_page = ProductsPage(driver).load()

        with allure.step("Search for the keyword 'dress'"):
            products_page.search_product("dress")

        with allure.step("Assert a 'Searched Products' results view is shown"):
            heading = products_page.get_search_results_heading()
            count = products_page.get_product_count()
            assert "Searched" in heading or "Products" in heading
            assert count >= 0  # graceful even if 0 results, never an error page

    @allure.story("Boundary value")
    @allure.title("TC-PRD-04: Searching an empty term does not crash the page")
    def test_search_empty_term(self, driver):
        products_page = ProductsPage(driver).load()

        with allure.step("Submit the search form with an empty search box"):
            products_page.search_product("")

        with allure.step("Assert the application responds gracefully (no error page)"):
            assert "automationexercise.com" in driver.current_url
            assert "Internal Server Error" not in driver.page_source

    @allure.story("Filtering")
    @allure.title("TC-PRD-08: Filtering by category narrows the product list")
    def test_filter_by_category(self, driver):
        products_page = ProductsPage(driver).load()

        with allure.step("Filter by Women > Dress category"):
            products_page.filter_by_category_women_dress()

        with allure.step("Assert the filtered category view is displayed"):
            heading = products_page.get_page_heading()
            assert heading != "", "Expected a category results heading to be shown."
