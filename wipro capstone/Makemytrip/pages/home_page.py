from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class HomePage(BasePage):
    # ------------------------------------------------------------------------
    # LOCATORS BANK (Verified against your DOM screenshots)
    # ------------------------------------------------------------------------
    # 1. Navigation Top Tabs [Image 1]
    LANDING_CONTAINER = (By.XPATH, "//div[@data-cy='landingContainer']")
    HOTELS_MODULE = (By.XPATH, "//li[@data-cy='menu_Hotels']")

    # 2. Destination Input Panel [Image 2]
    CITY_TAP_CONTAINER = (By.XPATH, "//span[@data-cy='hotelCityLabel']")
    CITY_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Where do you want to stay?']")
    FIRST_SUGGESTION = (By.XPATH,
                        "//ul[contains(@class,'react-autosuggest__suggestions-list')]/li[1] | //div[contains(@class,'autosuggest')]//li[1]")

    # 3. Calendar Selection Points
    CHECKIN_DATE_27 = (By.XPATH,
                       "//*[@id='checkin']//div[@aria-label='Wed May 27 2026'] | //div[@class='DayPicker-Day' and contains(@aria-label,'May 27 2026')]")
    CHECKOUT_DATE_30 = (By.XPATH,
                        "//*[@id='checkout']//div[@aria-label='Sat May 30 2026'] | //div[@class='DayPicker-Day' and contains(@aria-label,'May 30 2026')]")

    # 4. ROBUST SEARCH BUTTON XPATH (Targets both parent container & inner elements to be safe) [Image 4 Fix]
    HOTELS_SEARCH_BUTTON = (By.XPATH,
                            "//button[@data-cy='submit'] | //button[@id='hsearch_button'] | //button[contains(@class, 'widgetSearchBtn')]")

    # 5. Result Filters & Cards [Image 3]
    FIVE_STAR_FILTER = (By.XPATH,
                        "//span[@data-testid='checkboxFilter' and contains(., '5 Star')] | //label[contains(., '5 Star')]//span[contains(@class, 'check')]")
    FIRST_HOTEL_CARD = (By.XPATH,
                        "(//div[@id='hotelListingContainer']//div[contains(@class, 'ListingCard')]//a)[1] | (//div[contains(@id, 'ListingCard')]//h9)[1]")

    def __init__(self, driver, timeout=15):
        super().__init__(driver, timeout)

    # ------------------------------------------------------------------------
    # OPERATIONAL METHOD ENGINES
    # ------------------------------------------------------------------------
    def dismiss_login_popup(self):
        """Dismisses the initial background login intercept overlay safely."""
        try:
            time.sleep(4)
            if self.is_element_visible(self.LANDING_CONTAINER):
                overlay = self.driver.find_element(*self.LANDING_CONTAINER)
                self.driver.execute_script("arguments[0].click();", overlay)
                print("[INFO] Closed initial login overlay container background.")
                time.sleep(2)
        except Exception as e:
            print(f"[INFO] Popup overlay skip: {str(e)}")

    def click_hotels_module(self):
        """Navigates directly to the Hotels app space."""
        print("[INFO] Navigating to Hotels module...")
        hotels_element = self.wait.until(lambda d: d.find_element(*self.HOTELS_MODULE))
        self.driver.execute_script("arguments[0].click();", hotels_element)
        time.sleep(3)

    def search_hotel_destination(self, city_name):
        """Selects the destination city via the lookup component field."""
        print(f"[INFO] Entering city destination: {city_name}")
        city_trigger = self.wait.until(lambda d: d.find_element(*self.CITY_TAP_CONTAINER))
        self.driver.execute_script("arguments[0].click();", city_trigger)
        time.sleep(1.5)

        input_element = self.wait.until(lambda d: d.find_element(*self.CITY_INPUT_FIELD))
        input_element.send_keys(city_name)
        time.sleep(2.5)

        suggestion_item = self.wait.until(lambda d: d.find_element(*self.FIRST_SUGGESTION))
        self.driver.execute_script("arguments[0].click();", suggestion_item)
        time.sleep(2)

    def select_stay_dates(self):
        """Pins both targets on the interactive calendar."""
        print("[INFO] Selecting check-in date: May 27, 2026")
        checkin_el = self.wait.until(lambda d: d.find_element(*self.CHECKIN_DATE_27))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkin_el)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", checkin_el)
        time.sleep(1.5)

        print("[INFO] Selecting check-out date: May 30, 2026")
        checkout_el = self.wait.until(lambda d: d.find_element(*self.CHECKOUT_DATE_30))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkout_el)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", checkout_el)
        time.sleep(2)
        # Note: Avoid closing the calendar overlay manually, as the next step's scroll fixes layout focus issues.

    def trigger_search_query(self):
        """Triggers the search submission via the multi-matched button element."""
        print("[INFO] Submitting search criteria...")

        # Pull the button node explicitly from DOM
        search_btn = self.wait.until(lambda d: d.find_element(*self.HOTELS_SEARCH_BUTTON))

        # Bring it into viewport focus context, then force submit via JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", search_btn)

        print("[INFO] Search successfully executed!")
        time.sleep(6)  # Give listing interface room to settle and load the rows

    def apply_filters(self):
        """Checks the 5-Star luxury options checkbox filter."""
        print("[INFO] Applying '5 Star' rating filter category...")
        try:
            five_star_el = self.wait.until(lambda d: d.find_element(*self.FIVE_STAR_FILTER))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", five_star_el)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", five_star_el)
            print("[INFO] 5-Star filter applied successfully!")
            time.sleep(4)
        except Exception as e:
            print(f"[ERROR] Filter execution step issue: {str(e)}")
            raise e

    def select_first_hotel(self):
        """Clicks the top matching hotel card option from the remaining active grid array layout rows."""
        print("[INFO] Selecting the top matching hotel listing choice...")
        try:
            first_hotel = self.wait.until(lambda d: d.find_element(*self.FIRST_HOTEL_CARD))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_hotel)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", first_hotel)
            print("[INFO] First hotel item clicked!")
            time.sleep(4)
        except Exception as e:
            print(f"[ERROR] Listing card failure state: {str(e)}")
            raise e