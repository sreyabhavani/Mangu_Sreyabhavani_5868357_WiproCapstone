import os
from datetime import datetime
from utils.logger import AutomationLogger

# FIXED: Now uses the updated AutomationLogger class and method name
logger = AutomationLogger.get_logger("ScreenshotUtil")

class ScreenshotUtil:

    @staticmethod
    def capture(driver, name):

        screenshot_dir = "reports/screenshots"

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        screenshot_path = (
            f"{screenshot_dir}/"
            f"{name}_{timestamp}.png"
        )

        driver.save_screenshot(screenshot_path)

        logger.info(
            f"SCREENSHOT SAVED : {screenshot_path}"
        )

        return screenshot_path