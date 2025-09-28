from pages.login_page import LoginPage

class LoginKeywords:
    def __init__(self, login_page: LoginPage):
        """Takes LoginPage POM for keyword operations."""
        self.login_page = login_page

    def login_with_valid_credentials(self, username: str, password: str):
        """Complete login flow with valid credentials."""
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()

    def login_with_invalid_password(self, username: str, wrong_password: str):
        """Try login with wrong password and checks login button is disabled."""
        self.login_page.enter_username(username)
        self.login_page.enter_password(wrong_password)
        self.login_page.check_login_button_disabled()