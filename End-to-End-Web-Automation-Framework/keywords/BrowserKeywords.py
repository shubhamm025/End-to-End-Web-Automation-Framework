from core.browser_factory import BrowserFactory


class BrowserKeywords:
    """
    Public-facing browser actions for tests/keywords.
    Wraps BrowserFactory (composition) so that internal _ methods
    are hidden from tests.
    """

    def __init__(self):
        self._factory = BrowserFactory

    def open_browser(self, base_url: str, browser: str = "chrome", headless: bool = False):
        """
        Open a browser and navigate to the given URL.
        """
        return self._factory._open_application(browser, base_url, headless)

    def close_browser(self):
        """
        Close the current browser.
        """
        self._factory._quit_driver()

    def refresh_browser(self):
        """
        Refresh the current page.
        """
        driver = self._factory._get_driver()
        driver.refresh()

    def get_driver(self):
        """
        Get the active WebDriver instance.
        """
        return self._factory._get_driver()