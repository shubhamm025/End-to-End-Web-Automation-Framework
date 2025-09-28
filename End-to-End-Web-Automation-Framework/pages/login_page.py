from core.base_page import BasePage

class LoginPage(BasePage):

    def __init__(self, 
                parent: BasePage = None):
        super().__init__(parent,locator="//div[@class='orangehrm-login-slot-wrapper']")
        self.add_element(name="username",locator= "//input[@name='username']")
        self.add_element(name="password",locator="//input[@name='password']")
        self.add_element(name="login_btn", locator="//button[@type='submit']")


    @property
    def username(self) -> BasePage:
        return self.element("username")

    @property
    def password(self) -> BasePage:
        return self.element("password")

    @property
    def login_btn(self) -> BasePage:
        return self.element("login_btn")

    def enter_username(self, username: str):
        self.username.send_keys(username)

    def enter_password(self, password: str):
        self.password.send_keys(password)

    def click_login(self):
        self.login_btn.click()

    def is_login_button_enabled(self) -> bool:
        return self.login_btn.is_enabled()

    def check_login_button_disabled(self):
        if self.login_btn.is_enabled():
            raise Exception("Login button is enabled")
              
    def wait_until_login_page_exists(self):
        self._wait_until_exists()
