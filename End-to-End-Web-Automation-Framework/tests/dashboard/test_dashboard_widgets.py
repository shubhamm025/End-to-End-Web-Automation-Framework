import pytest
from pages.page_manager import PageManager
from variables  import  *

class TestDashboardWidgets:

    @pytest.fixture(scope="class", autouse=True)
    def suite_setup_and_teardown(self,pages: PageManager):
        """
        Suite-level setup/teardown.
        Open browser and login once before suite, close browser after suite.
        """
        # Suite setup
        pages.browser.open_browser(BASE_URL,BROWSER,HEADLESS)
        pages.login_keywords.login_with_valid_credentials(USERNAME,PASSWORD)
        yield
        # Suite teardown
        pages.browser.close_browser()


    @pytest.fixture(autouse=True)
    def test_setup_and_teardown(self, pages: PageManager):
        """
        Test-level setup/teardown.
        Runs before and after each test method.
        """
        # Test setup steps (if any specific preparation)
        yield
        # Test teardown → refresh app so next test starts clean
        pages.browser.refresh_browser()