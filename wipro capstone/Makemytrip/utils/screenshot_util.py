import os
import time

class ScreenshotUtils:
    @staticmethod
    def capture_screenshot(driver, name_prefix="Screenshot"):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshots/{name_prefix}_{timestamp}.png"
        driver.save_screenshot(filename)
        return filename