
import time
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException

from core.enums.wait_type import WaitType
from core.enums.identification_mode import IdentificationMode
from core.browser_factory import BrowserFactory
from selenium.webdriver.common.action_chains    import ActionChains

class BasePage:

    __timeout = 60
    __wait_time = 30
    __pooling_interval = 0.5

    def __init__(self,
                parent: "BasePage" = None,
                locator: str = "", 
                by: IdentificationMode = IdentificationMode.XPATH, 
                wait_type: WaitType = WaitType.NONE):
    
        self.locator = locator
        self.parent = parent
        self.by = by
        self.wait_type = wait_type
        self.element_registry = {}
    
    @property
    def wait_time(self) -> int:
        return self.__wait_time

    @property
    def driver(self) -> WebDriver:
        return BrowserFactory._get_driver()

    @property
    def pooling_interval(self) -> float:
        return self.__pooling_interval
    
    @property
    def timeout(self) -> int:
        return self.__timeout
    
    @property
    def full_locator(self) -> str:
        if not self.locator:
            raise ValueError("Locator not defined for this element.")

        # Only concatenate for XPath
        if self.by == IdentificationMode.XPATH and self.parent:
            parent_xpath = self.parent.full_locator.rstrip("/")
            child_xpath = self.locator.lstrip("/")
            return parent_xpath + child_xpath

        return self.locator
    

    @property
    def locator_strategy(self) -> str:
        mapping = {
            IdentificationMode.ID: By.ID,
            IdentificationMode.NAME: By.NAME,
            IdentificationMode.CSS: By.CSS_SELECTOR,
            IdentificationMode.XPATH: By.XPATH,
        }
        try:
            return mapping[self.by]
        except KeyError:
            raise NotImplementedError(f"Unknown identification mode {self.by}")
    
    def _find_element(self, locator: str = None, by: IdentificationMode = None, wait_type: WaitType = None):
        locator = locator or self.full_locator
        by = by or self.by
        wait_type = wait_type or self.wait_type
        strategy = self._get_locator_strategy(by)

        if wait_type == WaitType.NONE: 
            return self.driver.find_element(strategy, locator)
        elif wait_type == WaitType.CLICKABLE:
            return WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((strategy, locator)))
        elif wait_type == WaitType.VISIBLE:
            return WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((strategy, locator)))
        elif wait_type == WaitType.PRESENT:
            return WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((strategy, locator)))
        else:
            raise ValueError(f"Undefined wait type: {wait_type}")
    
    def _wait_until(self, condition, timeout: int = None):
        timeout = timeout if timeout is not None else self.wait_time
        return WebDriverWait(self.driver, timeout, poll_frequency=self.pooling_interval).until(condition)
    
    def _wait_until_exists(self, max_wait_time: int = 0) -> bool:
        timeout = max_wait_time if max_wait_time > 0 else self.wait_time
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self._exists():
                return True
            time.sleep(self.pooling_interval)
        raise TimeoutError(f"After {timeout} seconds the GUI object '{self.locator}' still did not exist.")


    def _click(self):
        try:
            self._wait_until_exists()
            self._find_element().click()
        except (StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException):
            try:
                print(f"Retrying click... Locator: {self.locator}, Strategy: {self.locator_strategy}")
                ActionChains(self.driver).move_to_element(self._find_element()).perform()
                self._find_element().click()
            except (StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException) as e:
                print(f"Click failed after retry. Locator: {self.locator}, Strategy: {self.locator_strategy}")
                raise e

    def _exists(self) -> bool:
        try:
            self.driver._find_element(self.locator_strategy, self.locator)
            return True
        except NoSuchElementException:
            return False

    def _send_keys(self, text: str):
        try:
            self._wait_until_exists()
            self._find_element().send_keys(text)
        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException) as e:
            print(f"Failed to send keys to element using locator: '{self.locator}' and strategy: '{self.locator_strategy}'")
            raise e

    def _get_locator_strategy(self, by: IdentificationMode) -> str:
        mapping = {
            IdentificationMode.ID: By.ID,
            IdentificationMode.NAME: By.NAME,
            IdentificationMode.CSS: By.CSS_SELECTOR,
            IdentificationMode.XPATH: By.XPATH,
        }
        try:
            return mapping[by]
        except KeyError:
            raise NotImplementedError(f"Unknown identification mode {by}")

    # ---- Element registry (public API) --------------------------------------------
    def add_element(self, name: str, locator: str, by: IdentificationMode = IdentificationMode.XPATH):
        """Register an element with name, locator, identification strategy, and optional parent context."""
        self.element_registry[name] = {
            "locator": locator,
            "by": by
        }

    def element(self, name: str) -> "BasePage":
        """Return a bound BasePage representing a registered element by name."""
        meta = self.element_registry.get(name)
        if not meta:
            raise KeyError(f"Element with name '{name}' not found in registry.")
        
        element = BasePage(
            locator=meta["locator"],
            by=meta["by"]
        )     
        return element

    # ---- Public fluent actions on bound element -----------------------------------


    def click(self):
       self._click()

    def send_keys(self, text: str):
        self._send_keys(text)


    def get_attribute(self, attribute: str) -> Optional[str]:
        self._wait_until_exists()
        element = self._find_element()
        return element.get_attribute(attribute) if element else None

    def is_visible(self) -> bool:
        try:
            self._wait_until(EC.visibility_of_element_located((self.locator_strategy, self.locator)))
            return True
        except Exception:
            return False

    def is_present(self) -> bool:
        return self._exists()
    
    def is_enabled(self) -> bool:
        try:
            self._find_element().is_enabled()
            return True
        except Exception:
            return False


    def wait_until_invisible(self):
        self._wait_until(EC.invisibility_of_element_located((self.locator_strategy, self.locator)))
    
    def wait_until_clickable(self):
        return self._wait_until(EC.element_to_be_clickable((self.locator_strategy, self.locator)))

    def check_exists(self):
        if not self._exists():
            raise AssertionError(f"The webelement '{self.locator}' using strategy '{self.locator_strategy}' should exist but does not.")
    
    def create_webelemet(self, locator:str = None):
        if locator == None:
            return BasePage(locator=self.full_locator)
        else:
            return BasePage(locator=f"{self.full_locator}{self.locator}")
        
    def create_webelemnt_with_index(self, index:int):
        return BasePage(locator=f"{self.full_locator}[{index}]")