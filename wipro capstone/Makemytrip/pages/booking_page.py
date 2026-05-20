from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class BookingPage(BasePage):
    # Locators matching the inspector mapping
    FIRST_NAME_INPUT = (By.ID, "fName")
    LAST_NAME_INPUT = (By.ID, "lName")
    EMAIL_INPUT = (By.ID, "email")
    MOBILE_INPUT = (By.ID, "mNo")

    # PAN Details Field Locator
    PAN_INPUT = (By.XPATH, "//input[@placeholder='ENTER PAN HERE' or contains(@id, 'pan')] | //input[@id='panCheck']")

    # Secure Trip radio toggle
    SECURE_TRIP_YES_RADIO = (By.XPATH,
                             "//*[contains(text(), 'Yes, secure my trip')] | //label[contains(., 'secure my trip')]")

    # FIXED: Targeting the exact class name and exact HTML text case from your newest screenshot
    CONTINUE_PAYMENT_BUTTON = (By.XPATH,
                               "//a[contains(@class, 'btnContinuePayment')] | //a[contains(text(), 'Pay Now')]")

    def remove_blocking_chat_widget(self):
        """Removes the chat assistant widget from the DOM view layer."""
        try:
            self.driver.execute_script(
                "let elem = document.querySelector('iframe[name=\"cambot\"], div[class*=\"clamped\"], [class*=\"askMeAnything\"]'); if(elem) { elem.remove(); }"
            )
        except:
            pass

    def fill_guest_details_from_csv(self, data_set):
        """Switches tabs, clears the chatbot, and enters traveler + PAN info from CSV."""
        self.log.info("Synchronizing tabs and switching to the final Review/Booking tab...")
        time.sleep(4)

        window_tabs = self.driver.window_handles
        if len(window_tabs) > 1:
            self.driver.switch_to.window(window_tabs[-1])

        self.remove_blocking_chat_widget()

        try:
            # 1. First Name
            csv_first_name = data_set['first_name']
            f_name_field = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
            )
            f_name_field.clear()
            f_name_field.send_keys(csv_first_name)

            # 2. Last Name
            csv_last_name = data_set['last_name']
            l_name_field = self.driver.find_element(*self.LAST_NAME_INPUT)
            l_name_field.clear()
            l_name_field.send_keys(csv_last_name)

            # 3. Optional Email & Mobile Fields
            if 'email' in data_set:
                self.driver.find_element(*self.EMAIL_INPUT).send_keys(data_set['email'])
            if 'mobile' in data_set:
                self.driver.find_element(*self.MOBILE_INPUT).send_keys(data_set['mobile'])

            # 4. PAN Details
            csv_pan = data_set['pan_number']
            pan_field = self.driver.find_element(*self.PAN_INPUT)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
            time.sleep(1)
            pan_field.clear()
            pan_field.send_keys(csv_pan)
            self.log.info(f"CSV READ: Filled PAN Details -> {csv_pan}")

        except KeyError as e:
            self.log.error(f"CSV DATA ERROR: Missing column header {str(e)}")
            raise e

    def handle_secure_trip_and_continue(self):
        """
        Progressively scrolls down, selects 'Yes, secure my trip.', and clicks 'PAY NOW'.
        """
        self.log.info("Initiating progressive scroll to load insurance and payment buttons...")

        # 1. Scroll down far enough to make the buttons render
        try:
            for i in range(5):
                self.driver.execute_script("window.scrollBy(0, 350);")
                time.sleep(1)
        except:
            pass

        self.remove_blocking_chat_widget()

        try:
            # 2. Select 'Yes, secure my trip.'
            self.log.info("Locating 'Yes, secure my trip.' radio button...")
            secure_toggle = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SECURE_TRIP_YES_RADIO)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", secure_toggle)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", secure_toggle)
            self.log.info("Successfully clicked Insurance Option!")
            time.sleep(2)

            # 3. Handle the 'Pay Now' Button Click
            self.log.info("Locating 'Pay Now' button...")
            continue_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CONTINUE_PAYMENT_BUTTON)
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
            time.sleep(1.5)

            # Use standard click first, fallback to JS click if intercepted
            try:
                continue_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", continue_btn)

            self.log.info("Successfully clicked PAY NOW! Awaiting gateway transition...")

            time.sleep(8)

        except Exception as e:
            self.log.error(f"Failed to click insurance or payment button: {str(e)}")
            raise e