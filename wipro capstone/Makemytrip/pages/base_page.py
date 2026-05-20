import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import AutomationLogger


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.log = AutomationLogger.get_logger(self.__class__.__name__)

        self.screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def take_screenshot(self, action_name):
        """Captures standard context images of the browser workspace."""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{action_name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        try:
            self.driver.save_screenshot(filepath)
            self.log.info(f"Screenshot successfully logged onto target path reference location: {filepath}")
        except Exception as e:
            self.log.error(f"Failed to extract and capture page layout snapshot sequence: {str(e)}")

    def is_element_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except:
            return False