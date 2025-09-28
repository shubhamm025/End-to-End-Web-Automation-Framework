import pytest
from pages.page_manager import PageManager
from variables  import  *
import allure

class TestLoginFlow:

    @pytest.fixture(autouse=True)
    def test_setup_and_teardown(self, pages: PageManager):
        """
        Test-level setup/teardown.
        Runs before and after each test method.
        """      
        pages.browser.open_browser(BASE_URL,BROWSER,HEADLESS)
        # Test setup steps (if any specific preparation)
        yield
        # Test teardown → refresh app so next test starts clean
        pages.browser.close_browser()
        
    @allure.title("Login with valid credentials")
    def test_login_with_valid_credentials(self,pages: PageManager):
        pages.login_keywords.login_with_valid_credentials(USERNAME, PASSWORD)


    @allure.title("Login with invalid credentials")
    def test_login_with_invalid_credentials(self,pages: PageManager):
        pages.login_page.enter_username(USERNAME)
        pages.login_page.enter_password('wrong_password')
        pages.login_page.click_login()
        pages.login_page.check_invalide_login_credentials_error_text('Invalid credentials')