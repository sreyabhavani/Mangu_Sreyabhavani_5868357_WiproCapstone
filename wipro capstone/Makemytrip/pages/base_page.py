from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click_element(self, locator):
        """Waits for an element to be clickable and clicks it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def is_element_visible(self, locator):
        """Checks if an element is visible on the DOM."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except:
            return False