"""
Pytest configuration & shared fixtures for the Selenium regression suite.

Run examples:
    pytest                                  # Chrome, headed
    pytest --browser=firefox                # Firefox
    pytest --browser=chrome --headless      # Chrome headless (used in CI)
"""

import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

BASE_URL = "https://automationexercise.com"


# --------------------------------------------------------------------------- #
# CLI options
# --------------------------------------------------------------------------- #
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                      help="Browser to run tests on: chrome | firefox | edge")
    parser.addoption("--headless", action="store_true", default=False,
                      help="Run the browser in headless mode")


# --------------------------------------------------------------------------- #
# Driver factory
# --------------------------------------------------------------------------- #
def _build_driver(browser_name, headless):
    browser_name = browser_name.lower()

    if browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        try:
            from webdriver_manager.firefox import GeckoDriverManager
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        except ImportError:
            driver = webdriver.Firefox(options=options)

    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        try:
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
        except ImportError:
            driver = webdriver.Edge(options=options)

    else:  # default: chrome
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except ImportError:
            driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(0)  # we rely on explicit waits in BasePage
    driver.maximize_window()
    return driver


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") or os.getenv("CI") == "true"

    drv = _build_driver(browser_name, headless)
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def base_url():
    return BASE_URL


# --------------------------------------------------------------------------- #
# Screenshot-on-failure + Allure attachment
# --------------------------------------------------------------------------- #
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
            try:
                driver.save_screenshot(screenshot_path)
                with open(screenshot_path, "rb") as f:
                    allure.attach(f.read(), name=f"{item.name}-failure",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass  # never let screenshot capture mask the real failure
