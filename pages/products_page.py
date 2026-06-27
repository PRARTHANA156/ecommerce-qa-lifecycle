"""ProductsPage — catalog grid, search, category/brand filters."""

from selenium.webdriver.common.by import By

from .base_page import BasePage

BASE_URL = "https://automationexercise.com"


class ProductsPage(BasePage):
    URL = BASE_URL + "/products"

    PAGE_TITLE = (By.CSS_SELECTOR, "h2.title.text-center")
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")

    PRODUCT_CARDS = (By.CSS_SELECTOR, "div.product-image-wrapper")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "div.productinfo p")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "div.productinfo h2")
    FIRST_VIEW_PRODUCT_LINK = (By.CSS_SELECTOR, "div.product-image-wrapper a[href*='/product_details/']")

    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "a.add-to-cart")
    MODAL_VIEW_CART_LINK = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")
    MODAL_CONTINUE_SHOPPING = (By.CSS_SELECTOR, "#cartModal button.close-modal")

    CATEGORY_PANEL = (By.ID, "accordian")
    CATEGORY_WOMEN_LINK = (By.CSS_SELECTOR, "a[href='#Women']")
    CATEGORY_WOMEN_DRESS_SUBLINK = (By.CSS_SELECTOR, "#Women a[href='/category_products/1']")

    BRANDS_PANEL = (By.CSS_SELECTOR, "div.brands_products")
    BRAND_POLO_LINK = (By.CSS_SELECTOR, "ul.brands-name a[href='/brand_products/Polo']")

    def load(self):
        self.open(self.URL)
        return self

    # --- Catalog -----------------------------------------------------------
    def get_product_count(self):
        return len(self.find_all(self.PRODUCT_CARDS))

    def get_page_heading(self):
        return self.get_text(self.PAGE_TITLE)

    def open_first_product_details(self):
        self.click(self.FIRST_VIEW_PRODUCT_LINK)
        return self

    # --- Search ------------------------------------------------------------
    def search_product(self, term):
        self.type_text(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)
        return self

    def get_search_results_heading(self):
        return self.get_text(self.PAGE_TITLE)

    # --- Add to cart ---------------------------------------------------------
    def add_first_product_to_cart(self):
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        self.driver.execute_script("arguments[0].click();", buttons[0])
        return self

    def add_nth_product_to_cart(self, index):
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        self.driver.execute_script("arguments[0].click();", buttons[index])
        return self

    def continue_shopping(self):
        self.click(self.MODAL_CONTINUE_SHOPPING)
        return self

    def view_cart_from_modal(self):
        self.click(self.MODAL_VIEW_CART_LINK)
        return self

    # --- Filters -------------------------------------------------------------
    def filter_by_category_women_dress(self):
        self.click(self.CATEGORY_WOMEN_LINK)
        self.click(self.CATEGORY_WOMEN_DRESS_SUBLINK)
        return self

    def filter_by_brand_polo(self):
        self.scroll_into_view(self.BRAND_POLO_LINK)
        self.click(self.BRAND_POLO_LINK)
        return self
