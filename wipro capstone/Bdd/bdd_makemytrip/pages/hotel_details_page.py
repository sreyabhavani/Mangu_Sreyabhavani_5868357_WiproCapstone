# pages/hotel_details_page.py
import time
from pages.base_page import BasePage
from locators.hotel_details_page_locators import HotelDetailsPageLocators
from utils.waits_util import WaitUtils

class HotelDetailsPage(BasePage):
    # Uses the constructor and self.log directly from BasePage automatically

    def handle_flexible_stay_overlay(self):
        try:
            time.sleep(2)
            skip_elements = self.driver.find_elements(*HotelDetailsPageLocators.POPUP_SKIP_BUTTON)
            for el in skip_elements:
                if el.is_displayed():
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(2)
                    return True
        except Exception:
            pass
        return False

    def apply_5_star_filter(self):
        self.handle_flexible_stay_overlay()
        self.log.info("Applying 5-Star hotel results modifier...")

        filter_element = None
        for locator in HotelDetailsPageLocators.FIVE_STAR_FILTERS:
            try:
                # Swapped out raw WebDriverWait for your WaitUtils handler
                filter_element = WaitUtils.wait_for_presence_of_element(self.driver, locator, timeout=5)
                if filter_element:
                    break
            except Exception:
                continue

        if filter_element:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", filter_element)
            time.sleep(5)

    def select_first_hotel(self):
        self.handle_flexible_stay_overlay()
        self.log.info("Selecting primary top-listed hotel choice card...")

        hotel_card = None
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                elements = self.driver.find_elements(*HotelDetailsPageLocators.EXACT_HOTEL_LINK)
                if not elements:
                    elements = self.driver.find_elements(*HotelDetailsPageLocators.FALLBACK_HOTEL_LINK)
                if elements and elements[0].is_enabled():
                    hotel_card = elements[0]
                    break
            except Exception:
                pass
            time.sleep(1)

        if not hotel_card:
            raise Exception("Core Automation Error: Could not resolve a clickable 5-star hotel choice on the grid.")

        target_href = hotel_card.get_attribute("href")
        if target_href:
            self.driver.get(target_href)
            time.sleep(6)
        else:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hotel_card)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", hotel_card)
            time.sleep(5)

    def click_book_now_on_details_page(self):
        self.log.info("Synchronizing tab session instances...")
        time.sleep(4)
        window_tabs = self.driver.window_handles

        if len(window_tabs) > 1:
            self.driver.switch_to.window(window_tabs[-1])
            time.sleep(4)

        try:
            self.driver.execute_script("window.scrollTo(0, 250);")
            time.sleep(2)
        except Exception:
            pass

        book_action_trigger = None
        for strategy in HotelDetailsPageLocators.BOOK_NOW_LOCATORS:
            try:
                # Replaced raw driver wait with your WaitUtils helper
                book_action_trigger = WaitUtils.wait_for_presence_of_element(self.driver, strategy, timeout=10)
                if book_action_trigger:
                    break
            except Exception:
                continue

        if not book_action_trigger:
            raise Exception("Validation Block: The primary action trigger element was not resolved.")

        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", book_action_trigger)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", book_action_trigger)
            time.sleep(5)
        except Exception as e:
            self.log.error(f"Failed to click booking button: {str(e)}")
            raise e