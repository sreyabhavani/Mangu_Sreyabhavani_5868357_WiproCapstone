import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger("HotelResultsPage")


class HotelResultsPage(BasePage):
    # Selectors parsed from your application UI viewports
    FLEXIBLE_STAY_SKIP_BTN = (By.XPATH, "//span[text()='Skip'] | //p[contains(text(),'Skip')]")
    FIVE_STAR_FILTER = (By.XPATH, "//span[contains(text(), '5 Star')] | //label[contains(., '5 Star')]")
    PRICE_BUDGET_FILTER = (By.XPATH, "//span[contains(text(), '4000-8000')] | //label[contains(., '4000-8000')]")
    FIRST_HOTEL_CARD = (By.XPATH,
                        "(//div[contains(@class, 'hotelListing')]//a | //div[contains(@id, 'Listing_item')])[1]")

    def skip_flexible_stay_popup(self):
        try:
            log.info("Checking for 'Flexible Stay' modal overlay popup...")
            element = self.wait.until(EC.element_to_be_clickable(self.FLEXIBLE_STAY_SKIP_BTN))
            element.click()
            log.info("Successfully skipped flexible stay popup.")
        except Exception:
            log.info("No modal overlay intercepted the view layer this session.")

    def apply_filters_and_select_first_hotel(self):
        # 1. Apply Filters
        log.info("Applying 5 Star and Price budget range filters...")
        self.click_element(self.FIVE_STAR_FILTER)
        time.sleep(2)  # Give DOM a brief moment to refresh listings
        self.click_element(self.PRICE_BUDGET_FILTER)
        time.sleep(3)  # Wait for AJAX hotel list refresh to settle

        # 2. Track Window Handles before click action
        original_window = self.driver.current_window_handle
        all_before_click = self.driver.window_handles
        log.info(f"Initial active window handle session count: {len(all_before_click)}")

        # 3. Fire the click event on the first listing card
        log.info("Clicking the first available hotel card listing...")
        self.click_element(self.FIRST_HOTEL_CARD)

        # 4. Wait explicitly for the new tab handle to materialize
        try:
            self.wait.until(lambda d: len(d.window_handles) > len(all_before_click))
            all_after_click = self.driver.window_handles
            log.info(f"Post-click active window handle session count: {len(all_after_click)}")

            # Find the new handle and switch to it
            for handle in all_after_click:
                if handle != original_window:
                    self.driver.switch_to.window(handle)
                    log.info("Successfully switched Selenium context driver focus to the new Hotel Details tab.")
                    break

            # Confirm document ready state on the new page view layer
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            log.info(f"Current active page title is now: {self.driver.title}")

        except Exception as e:
            log.error("Failed to detect or switch focus to the newly opened hotel details browser window tab.")
            raise e