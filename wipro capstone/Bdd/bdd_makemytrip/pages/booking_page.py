# pages/booking_page.py
import time
from pages.base_page import BasePage
from locators.booking_page_locators import BookingPageLocators
from utils.waits_util import WaitUtils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingPage(BasePage):

    def remove_blocking_chat_widget(self):
        try:
            self.driver.execute_script(
                "let elem = document.querySelector('iframe[name=\"cambot\"], div[class*=\"clamped\"], [class*=\"askMeAnything\"]'); if(elem) { elem.remove(); }"
            )
        except Exception:
            pass

    # --- UPDATED: Combined Method for Positive & Negative ---
    def fill_guest_details(self, data_set):
        """Fills form fields based on provided data. If value is None/Empty, it skips that field."""
        self.log.info("Filling guest details...")

        # Helper to safely enter data
        def enter_data(locator, value):
            if value:
                field = WaitUtils.wait_for_element_visible(self.driver, locator)
                field.clear()
                field.send_keys(value)

        enter_data(BookingPageLocators.FIRST_NAME_INPUT, data_set.get('firstName'))
        enter_data(BookingPageLocators.LAST_NAME_INPUT, data_set.get('lastName'))
        enter_data(BookingPageLocators.EMAIL_INPUT, data_set.get('email'))
        enter_data(BookingPageLocators.MOBILE_INPUT, data_set.get('mobileNumber'))
        enter_data(BookingPageLocators.PAN_INPUT, data_set.get('panNumber'))

    # --- NEW: Methods for Negative Test Assertions ---
    def verify_validation_message(self, expected_message):
        """Verifies an error message is displayed on the screen."""
        self.log.info(f"Verifying error message: {expected_message}")
        # Dynamically create locator for the error text
        xpath = f"//*[contains(text(), '{expected_message}')]"
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            assert element.is_displayed(), f"Validation message '{expected_message}' is not visible."
        except Exception:
            raise AssertionError(f"Validation message '{expected_message}' was not found on the page.")

    def verify_on_page(self, page_identifier):
        """Verifies the user has not transitioned to the payment gateway."""
        self.log.info(f"Checking if user is still on {page_identifier}")
        assert page_identifier in self.driver.current_url, \
            f"Expected to be on {page_identifier}, but current URL is {self.driver.current_url}"

    # --- EXISTING: Method for Positive Completion ---
    def handle_secure_trip_and_continue(self):
        self.log.info("Finalizing: Selecting insurance and paying...")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 500);")
        time.sleep(2)
        self.remove_blocking_chat_widget()

        secure_toggle = WaitUtils.wait_for_presence_of_element(self.driver, BookingPageLocators.SECURE_TRIP_YES_RADIO)
        self.driver.execute_script("arguments[0].click();", secure_toggle)

        continue_btn = WaitUtils.wait_for_presence_of_element(self.driver, BookingPageLocators.CONTINUE_PAYMENT_BUTTON)
        self.driver.execute_script("arguments[0].click();", continue_btn)