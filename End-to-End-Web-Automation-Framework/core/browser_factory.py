import threading
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class BrowserFactory:
    """
    Thread-safe BrowserFactory for parallel test execution.

    Each thread maintains its own WebDriver instance to prevent conflicts during
    concurrent test execution. Supports Chrome, Firefox, and Edge browsers.
    """

    _drivers = threading.local()

    @staticmethod
    def _create_chrome_driver(headless: bool) -> WebDriver:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(service=ChromeService(), options=options)

    @staticmethod
    def _create_firefox_driver(headless: bool) -> WebDriver:
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(service=FirefoxService(), options=options)

    @staticmethod
    def _create_edge_driver(headless: bool) -> WebDriver:
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Edge(service=EdgeService(), options=options)

    @staticmethod
    def _open_application(browser: str = "chrome", base_url: str | None = None, headless: bool = False) -> WebDriver:
        """
        Initializes a WebDriver for the current thread.

        Args:
            browser (str): Browser type ('chrome', 'firefox', 'edge').
            base_url (str | None): URL to open after browser launch.
            headless (bool): Whether to run browser in headless mode.

        Returns:
            WebDriver: Thread-local WebDriver instance.
        """
        if hasattr(BrowserFactory._drivers, "driver"):
            return BrowserFactory._drivers.driver

        browser = browser.lower()
        driver: WebDriver

        if browser == "chrome":
            driver = BrowserFactory._create_chrome_driver(headless)
        elif browser == "firefox":
            driver = BrowserFactory._create_firefox_driver(headless)
        elif browser == "edge":
            driver = BrowserFactory._create_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        if base_url:
            driver.get(base_url)

        BrowserFactory._drivers.driver = driver
        return driver

    @staticmethod
    def _get_driver() -> WebDriver:
        if not hasattr(BrowserFactory._drivers, "driver"):
            raise RuntimeError("Driver not initialized. Call open_application() first.")
        return BrowserFactory._drivers.driver


    @staticmethod
    def _quit_driver():
        driver = getattr(BrowserFactory._drivers, "driver", None)
        if driver:
            driver.quit()
            delattr(BrowserFactory._drivers, "driver")