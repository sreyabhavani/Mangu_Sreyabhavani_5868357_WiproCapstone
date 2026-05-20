from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import time
import random


class HomePage(BasePage):
    # ------------------------------------------------------------------------
    # LOCATORS BANK (Mapped dynamically across execution screens)
    # ------------------------------------------------------------------------
    LANDING_CONTAINER = (By.XPATH, "//div[@data-cy='landingContainer']")
    HOTELS_MODULE = (By.XPATH, "//li[@data-cy='menu_Hotels']")

    CITY_TAP_CONTAINER = (By.XPATH, "//span[@data-cy='hotelCityLabel']")
    CITY_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Where do you want to stay?']")
    FIRST_SUGGESTION = (By.XPATH,
                        "//ul[contains(@class,'react-autosuggest__suggestions-list')]/li[1] | //div[contains(@class,'autosuggest')]//li[1] | //p[contains(@class,'suggestion')][1]")

    CHECKIN_DATE_27 = (By.XPATH,
                       "//div[contains(@aria-label,'May 27 2026')] | //div[@class='DayPicker-Day' and .//p[text()='27']]")
    CHECKOUT_DATE_30 = (By.XPATH,
                        "//div[contains(@aria-label,'May 30 2026')] | //div[@class='DayPicker-Day' and .//p[text()='30']]")

    GUESTS_APPLY_BUTTON = (By.XPATH,
                           "//button[@data-cy='doneBtn'] | //button[contains(@class, 'btnApplyPersons')] | //button[text()='APPLY']")
    HOTELS_SEARCH_BUTTON = (By.XPATH,
                            "//button[@data-cy='submit'] | //button[@id='hsw_search_button'] | //button[contains(@class, 'widgetSearchBtn')]")

    FLEXIBLE_STAY_MODAL = (By.XPATH,
                           "//div[contains(@class, 'trueFlexiModal')] | //div[@id='portal-root']//div[contains(@class, 'modalContainer')]")
    MODAL_SKIP_BUTTON = (By.XPATH,
                         "//span[text()='SKIP'] | //span[contains(@class, 'text') and text()='SKIP'] | //div[contains(@class, 'trueFlexiModal')]//span[contains(text(), 'SKIP')]")

    # Dynamic filter paths mapping 5-Star checkboxes across multiple viewport resolutions
    FIVE_STAR_FILTER = (By.XPATH,
                        "//span[@data-testid='checkboxFilter' and contains(., '5 Star')] | //label[contains(., '5 Star')]//span[contains(@class, 'check')] | //li[contains(., '5 Star')]//input[@type='checkbox']")
    FIRST_HOTEL_CARD = (By.XPATH,
                        "(//div[@id='hotelListingContainer']//div[contains(@class, 'ListingCard')]//a)[1] | (//div[contains(@id, 'ListingCard')]//h9)[1] | (//div[contains(@class, 'ListingCard')])[1]")

    def dismiss_login_popup(self):
        self.log.info("Checking for the presence of the authentication intercept overlay frame...")
        try:
            time.sleep(3)
            if self.is_element_visible(self.LANDING_CONTAINER):
                overlay = self.driver.find_element(*self.LANDING_CONTAINER)
                self.driver.execute_script("arguments[0].click();", overlay)
                self.log.info("Authentication layout modal dismissed successfully.")
                time.sleep(1.5)
        except Exception as e:
            self.log.warning(f"Initial overlay intercept processing skipped: {str(e)}")

    def click_hotels_module(self):
        self.log.info("Navigating explicitly into the MakeMyTrip Hotels workspace panel module...")
        hotels_element = self.wait.until(EC.element_to_be_clickable(self.HOTELS_MODULE))
        hotels_element.click()
        self.take_screenshot("Hotels_Module_Loaded")

    def search_hotel_destination(self, city_name):
        """Brings the location fields into focus securely after the tab view reloads
        to completely eliminate stale element reference errors.
        """
        self.log.info(f"Opening query selection widget and inputting location details: {city_name}")

        # 1. Clear buffer: Allows the DOM to fully detach old nodes from the previous page view
        time.sleep(3)

        # 2. Fetch fresh element reference immediately after the wait
        city_trigger = self.wait.until(EC.presence_of_element_located(self.CITY_TAP_CONTAINER))
        try:
            city_trigger.click()
        except Exception:
            self.log.info("Native city selection field click intercepted. Forcing JavaScript click fallback...")
            self.driver.execute_script("arguments[0].click();", city_trigger)
        time.sleep(1.5)

        # 3. Input target destination parameters safely
        input_element = self.wait.until(EC.visibility_of_element_located(self.CITY_INPUT_FIELD))
        input_element.clear()
        for char in city_name:
            input_element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        time.sleep(2)

        # 4. Confirm dynamic lookup selection drop-down option
        suggestion_item = self.wait.until(EC.element_to_be_clickable(self.FIRST_SUGGESTION))
        suggestion_item.click()
        self.log.info(f"Successfully selected destination choice parameter option for: {city_name}")
    def select_stay_dates(self):
        self.log.info("Pinning check-in calendar grid coordinates target date: May 27, 2026")
        checkin_el = self.wait.until(EC.presence_of_element_located(self.CHECKIN_DATE_27))
        try:
            checkin_el.click()
        except Exception:
            self.log.info("Native check-in click intercepted by overlay. Executing JavaScript fallback...")
            self.driver.execute_script("arguments[0].click();", checkin_el)
        time.sleep(1)

        self.log.info("Pinning check-out calendar grid coordinates target date: May 30, 2026")
        checkout_el = self.wait.until(EC.presence_of_element_located(self.CHECKOUT_DATE_30))
        try:
            checkout_el.click()
        except Exception:
            self.log.info("Native check-out click intercepted by overlay. Executing JavaScript fallback...")
            self.driver.execute_script("arguments[0].click();", checkout_el)
        time.sleep(1)
        self.take_screenshot("Calendar_Dates_Selected")

    def configure_guests_and_apply(self):
        self.log.info("Validating guest matrix dimensions drawer and applying selection states...")
        try:
            apply_btn = self.wait.until(EC.presence_of_element_located(self.GUESTS_APPLY_BUTTON))
            self.driver.execute_script("arguments[0].click();", apply_btn)
            time.sleep(1)
        except Exception as e:
            self.log.warning(f"Guest drawer interactions processed via default inline states: {str(e)}")

    def trigger_search_query_negative_bypass(self):
        self.log.info(
            "Submitting query information criteria parameters to initialize compilation workflow execution...")
        search_btn = self.wait.until(EC.element_to_be_clickable(self.HOTELS_SEARCH_BUTTON))

        actions = ActionChains(self.driver)
        actions.move_to_element(search_btn).click().perform()
        time.sleep(3)

        generated_url = self.driver.current_url
        self.log.info(f"Captured current address path query parameters string: {generated_url}")
        self.take_screenshot("Search_Submission_200_OK_State")

        self.log.info("Executing URL direct-load escape bypass sequence to dodge direct raw API rendering faults...")
        self.driver.get(generated_url)
        time.sleep(5)

    def handle_flexible_stay_overlay(self):
        try:
            self.log.info("Scanning layout for promotional modal window elements...")
            time.sleep(2)
            if self.is_element_visible(self.FLEXIBLE_STAY_MODAL) or "trueFlexiModal" in self.driver.page_source:
                self.log.info(
                    "Promotional overlay 'Make Your Stay More Flexible' spotted! Dismissing via SKIP button...")
                self.take_screenshot("Flexibility_Popup_Observed")
                skip_btn = self.wait.until(EC.element_to_be_clickable(self.MODAL_SKIP_BUTTON))
                self.driver.execute_script("arguments[0].click();", skip_btn)
                self.log.info("Promotional modal successfully cleared from the storefront UI viewport view.")
                time.sleep(1.5)
        except Exception as e:
            self.log.info(f"Flexibility popups check sequence executed clear without blocks: {str(e)}")

    def apply_filters(self):
        """Filters search results safely after explicitly verifying page results initialization."""
        self.handle_flexible_stay_overlay()

        # 1. NEW: Explicitly wait for the hotel results layout or grid skeleton container to show up
        listing_anchor = (By.XPATH,
                          "//div[@id='hotelListingContainer'] | //div[contains(@class, 'hotelListing')] | //div[contains(@id, 'ListingCard')]")
        self.log.info("Waiting for hotel listing page layout cards to finish rendering on screen...")
        try:
            self.wait.until(EC.presence_of_element_located(listing_anchor))
            time.sleep(4)  # Settle down UI thread before attempting filters interaction
        except Exception:
            self.log.warning("Hotel container loading state delayed. Proceeding with filter search...")

        self.log.info("Applying standard '5 Star' accommodation quality score selection matrix filters...")
        try:
            # 2. Grab the element safely using presence bounds verification
            five_star_el = self.wait.until(EC.presence_of_element_located(self.FIVE_STAR_FILTER))

            # Scroll filter clean into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", five_star_el)
            time.sleep(1)

            # 3. Use JS Click strategy to override tracking blocks or transparent pop-up interferences
            self.driver.execute_script("arguments[0].click();", five_star_el)
            self.log.info("5 Star properties query parameter rules applied successfully via JS callback execution.")

            time.sleep(4)  # Wait for listing results refresh animation loop
            self.take_screenshot("Five_Star_Filter_Applied")
        except Exception as e:
            self.log.error(f"Failed to locate or check target rating filter components: {str(e)}")
            self.take_screenshot("Failed_Filter_Application_State")
            raise e

    def select_first_hotel(self):
        self.log.info("Extracting the primary premium choice hotel item row card details...")
        try:
            first_hotel = self.wait.until(EC.presence_of_element_located(self.FIRST_HOTEL_CARD))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_hotel)
            time.sleep(1)

            # Use JS execution trigger to launch the secondary details tab cleanly
            self.driver.execute_script("arguments[0].click();", first_hotel)
            self.log.info("Primary hotel element item activated via driver action event sequence.")
            time.sleep(4)
        except Exception as e:
            self.log.error(f"Target listing presentation data item could not be selected: {str(e)}")
            raise e