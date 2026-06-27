"""
BasePage
========
Parent class for every Page Object. Centralizes explicit waits, common
interactions, and screenshot capture so individual page classes stay thin
and only describe *what* is on the page, not *how* to wait for it.
"""

import os
import time

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

DEFAULT_TIMEOUT = 15


class BasePage:
    """Common functionality shared by all Page Objects."""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = DEFAULT_TIMEOUT

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #
    def open(self, url):
        self.driver.get(url)
        return self

    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        return self.driver.current_url

    # ------------------------------------------------------------------ #
    # Waits / finders
    # ------------------------------------------------------------------ #
    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    def find(self, locator, timeout=None):
        """Wait until the element is present, then return it."""
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def find_visible(self, locator, timeout=None):
        """Wait until the element is visible, then return it."""
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator, timeout=None):
        """Wait until the element is clickable, then return it."""
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def find_all(self, locator, timeout=None):
        """Wait until at least one element is present, return the full list."""
        self._wait(timeout).until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def is_visible(self, locator, timeout=5):
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_present(self, locator, timeout=5):
        try:
            self._wait(timeout).until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, fragment, timeout=None):
        return self._wait(timeout).until(EC.url_contains(fragment))

    # ------------------------------------------------------------------ #
    # Interactions
    # ------------------------------------------------------------------ #
    def click(self, locator, timeout=None):
        element = self.find_clickable(locator, timeout)
        try:
            element.click()
        except StaleElementReferenceException:
            element = self.find_clickable(locator, timeout)
            element.click()
        return self

    def type_text(self, locator, text, clear_first=True, timeout=None):
        element = self.find_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator, timeout=None):
        return self.find_visible(locator, timeout).text.strip()

    def scroll_into_view(self, locator, timeout=None):
        element = self.find(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.2)
        return element

    def hover(self, locator, timeout=None):
        from selenium.webdriver.common.action_chains import ActionChains

        element = self.find_visible(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()
        return self

    # ------------------------------------------------------------------ #
    # Evidence / debugging
    # ------------------------------------------------------------------ #
    def take_screenshot(self, name):
        """Save a PNG screenshot under /screenshots and return its path."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        safe_name = name.replace(" ", "_").replace("/", "_")
        path = os.path.join(SCREENSHOT_DIR, f"{safe_name}_{timestamp}.png")
        self.driver.save_screenshot(path)
        return path
