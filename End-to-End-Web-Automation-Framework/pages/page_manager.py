from keywords.BrowserKeywords import BrowserKeywords
from keywords.LoginPageKeywords import LoginKeywords
from pages.login_page import LoginPage

class PageManager:
    """Central access point for all Page Objects and Keywords."""

    def __init__(self):
        self.login_page = LoginPage()
        self.browser = BrowserKeywords()
        self.login_keywords = LoginKeywords(self.login_page)
        