from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class HotelDetailsPage(BasePage):
    POPUP_SKIP_BUTTON = (By.XPATH, "//span[text()='SKIP' or text()='Skip'] | //p[text()='SKIP']")

    FIVE_STAR_FILTERS = [
        (By.XPATH, "//span[text()='5 Star']"),
        (By.XPATH, "//label[contains(., '5 Star')]"),
        (By.XPATH, "//label[contains(@for, '5')]")
    ]

    EXACT_HOTEL_LINK = (By.XPATH, "//div[@id='Listing_hotel_0']//a | //div[@id='Listing_hotel_0']/a")
    FALLBACK_HOTEL_LINK = (By.XPATH, "(//a[contains(@href, 'hotel-details')])[1]")

    # Explicitly matching 'BOOK THIS NOW' as seen in the screenshots
    BOOK_NOW_LOCATORS = [
        (By.XPATH, "//button[contains(., 'BOOK THIS NOW')]"),
        (By.XPATH, "//a[contains(., 'BOOK THIS NOW')]"),
        (By.XPATH, "//*[contains(text(), 'BOOK THIS NOW')]"),
        (By.XPATH, "//button[text()='BOOK NOW' or text()='Book Now']")
    ]

    def handle_flexible_stay_overlay(self):
        try:
            time.sleep(2)
            skip_elements = self.driver.find_elements(*self.POPUP_SKIP_BUTTON)
            for el in skip_elements:
                if el.is_displayed():
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(2)
                    return True
        except:
            pass
        return False

    def apply_5_star_filter(self):
        self.handle_flexible_stay_overlay()
        self.log.info("Applying 5-Star hotel results modifier...")

        filter_element = None
        for locator in self.FIVE_STAR_FILTERS:
            try:
                filter_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(locator)
                )
                if filter_element:
                    break
            except:
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
                elements = self.driver.find_elements(*self.EXACT_HOTEL_LINK)
                if not elements:
                    elements = self.driver.find_elements(*self.FALLBACK_HOTEL_LINK)
                if elements and elements[0].is_enabled():
                    hotel_card = elements[0]
                    break
            except:
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
        """Handles tab synchronization, scrolls explicitly to bypass the AI overlay, and clicks."""
        self.log.info("Synchronizing tab session instances...")
        time.sleep(4)
        window_tabs = self.driver.window_handles

        if len(window_tabs) > 1:
            self.driver.switch_to.window(window_tabs[-1])
            self.log.info(f"Context redirected to hotel profile workspace tab: {self.driver.current_url}")
            time.sleep(4)

        # FIXED: Scroll the page up slightly/reposition viewport so the AI overlay doesn't cover the button
        self.log.info("Adjusting viewport positioning to clear the floating AI overlay view block...")
        try:
            self.driver.execute_script("window.scrollTo(0, 250);")
            time.sleep(2)
        except:
            pass

        book_action_trigger = None
        for strategy in self.BOOK_NOW_LOCATORS:
            try:
                book_action_trigger = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(strategy)
                )
                if book_action_trigger:
                    break
            except:
                continue

        if not book_action_trigger:
            self.take_screenshot("Missing_Book_Now_Button_Layout")
            raise Exception(
                "Validation Block: The primary action trigger element 'BOOK THIS NOW' was not resolved within this context window.")

        try:
            # Scroll the element directly into view focus, then offset it slightly if needed
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", book_action_trigger)
            time.sleep(1.5)

            # Fire click via JS to prevent element click intercepted exceptions from the overlay
            self.log.info("Clicking on 'BOOK THIS NOW' element...")
            self.driver.execute_script("arguments[0].click();", book_action_trigger)
            self.log.info("Successfully pushed past the hotel details view!")
            time.sleep(5)
        except Exception as e:
            self.log.error(f"Failed to click booking button: {str(e)}")
            raise e