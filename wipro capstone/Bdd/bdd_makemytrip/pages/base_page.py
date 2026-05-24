# pages/base_page.py
from utils.logger import LogGen
from utils.waits_util import WaitUtils  # Fixed the broken import module name

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.log = LogGen.loggen()  # Defined as self.log to match across child pages

    def click(self, locator):
        """Intercepts and ensures an element is completely clickable prior to routing an interaction execution."""
        WaitUtils.wait_for_element_clickable(self.driver, locator).click()

    def enter_text(self, locator, text):
        """Guarantees visibility constraints are cleared, flushes current values, and inputs new strings safely."""
        element = WaitUtils.wait_for_element_visible(self.driver, locator)
        element.clear()
        element.send_keys(text)

    def is_displayed(self, locator):
        """Verifies if an element is currently rendered on screen without throwing unhandled exceptions."""
        try:
            return WaitUtils.wait_for_element_visible(self.driver, locator).is_displayed()
        except Exception:
            return False

    def is_element_visible(self, locator):
        """Helper method to determine quick visibility boundaries without unhandled crashes."""
        try:
            return WaitUtils.wait_for_element_visible(self.driver, locator).is_displayed()
        except Exception:
            return False