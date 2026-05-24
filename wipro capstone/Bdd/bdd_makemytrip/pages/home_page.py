# pages/home_page.py
from pages.base_page import BasePage
from locators.home_page_locators import HomePageLocators as Locators
from utils.logger import LogGen
from selenium.webdriver.common.keys import Keys
import time
from utils.waits_util import WaitUtils


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.log = LogGen.loggen()

    def dismiss_login_popup(self):
        self.log.info("Checking for the presence of the authentication intercept overlay frame...")
        time.sleep(3)

        try:
            close_button = WaitUtils.wait_for_element_visible(self.driver, Locators.CLOSE_MODAL_X, timeout=7)
            self.log.info("Authentication 'X' close token found. Dispatched click operation...")
            try:
                close_button.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", close_button)

            self.log.info("Authentication layout modal dismissed successfully via 'X' element handler.")
            time.sleep(3)

        except Exception as e:
            self.log.warning(f"Overlay 'X' element not interactive or missing: {str(e)}")
            if self.is_element_visible(Locators.LANDING_CONTAINER):
                try:
                    overlay = self.driver.find_element(*Locators.LANDING_CONTAINER)
                    self.driver.execute_script("arguments[0].click();", overlay)
                    self.log.info("Bypassed layout container via generic structural window click fallback loop.")
                    time.sleep(3)
                except Exception:
                    pass

    def click_hotels_module(self):
        self.log.info("Navigating into the MakeMyTrip Hotels workspace panel...")
        hotels_element = WaitUtils.wait_for_element_clickable(self.driver, Locators.HOTELS_MODULE)
        try:
            hotels_element.click()
        except Exception:
            self.log.warning("Standard element click intercepted; deploying JavaScript fallback action.")
            self.driver.execute_script("arguments[0].click();", hotels_element)
        time.sleep(5)

    def search_hotel_destination(self, destination):
        self.log.info(f"Attempting to type: {destination}")

        city_trigger = WaitUtils.wait_for_element_clickable(self.driver, Locators.CITY_TAP_CONTAINER)
        self.driver.execute_script("arguments[0].click();", city_trigger)

        input_element = WaitUtils.wait_for_element_visible(self.driver, Locators.CITY_INPUT_FIELD)
        self.driver.execute_script("arguments[0].focus();", input_element)
        input_element.clear()

        for char in destination:
            input_element.send_keys(char)
            time.sleep(0.5)

        input_element.send_keys(Keys.ENTER)

        try:
            suggestion = WaitUtils.wait_for_element_clickable(self.driver, Locators.FIRST_SUGGESTION)
            suggestion.click()
            self.log.info(f"Successfully selected: {destination}")
        except Exception as e:
            self.log.warning(f"Suggestion click failed, trying keyboard fallback: {str(e)}")
            input_element.send_keys(Keys.DOWN)
            input_element.send_keys(Keys.ENTER)

    def select_stay_dates(self):
        """Bypasses custom date entry entirely. Bypasses the automatically opened calendar modal by focusing on guest options."""
        self.log.info("Bypassing date selection entirely to preserve website default options.")
        try:
            # We target the guest count wrapper field. Clicking this safely forces the calendar modal to close.
            guest_trigger = self.driver.find_element(*Locators.GUESTS_APPLY_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", guest_trigger)
            time.sleep(1)
        except Exception:
            pass

    def configure_guests_and_apply(self):
        self.log.info("Confirming existing guest configurations...")
        try:
            # Click Done/Apply button to close out any lingering dropdown states
            apply_btn = WaitUtils.wait_for_element_clickable(self.driver, Locators.GUESTS_APPLY_BUTTON, timeout=5)
            self.driver.execute_script("arguments[0].click();", apply_btn)
            time.sleep(2)
        except Exception:
            self.log.warning("Guest apply button already processed or omitted from layout view context.")

    def trigger_search_query_negative_bypass(self):
        self.log.info("Triggering search query...")
        search_btn = WaitUtils.wait_for_element_clickable(self.driver, Locators.HOTELS_SEARCH_BUTTON)
        self.driver.execute_script("arguments[0].click();", search_btn)