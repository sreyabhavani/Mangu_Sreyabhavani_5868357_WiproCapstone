from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class PaymentPage(BasePage):
    # Target the exact list-item container from your screenshot
    CREDIT_DEBIT_CARD_TAB = (By.XPATH, "//li[@data-testid='paymode-container' and contains(., 'Credit & Debit')]")

    # Highly flexible locators to catch the exact fields even if MMT changes their IDs
    CARD_NUMBER_INPUT = (By.XPATH,
                         "//input[@id='cardNumber' or @name='cardNumber' or contains(@placeholder, 'Card Number')]")
    CARD_NAME_INPUT = (By.XPATH,
                       "//input[@id='cardName' or @id='nameOnCard' or @name='nameOnCard' or contains(@placeholder, 'Name on')]")

    # Expiry fields might be dropdowns (select) or text inputs (input)
    EXPIRY_MONTH_SELECT = (By.XPATH, "//*[@id='expiryMonth' or contains(@placeholder, 'MM')]")
    EXPIRY_YEAR_SELECT = (By.XPATH, "//*[@id='expiryYear' or contains(@placeholder, 'YY')]")
    CVV_INPUT = (By.XPATH, "//input[@id='cvv' or @name='cvv' or contains(@placeholder, 'CVV')]")

    def select_credit_debit_card_option(self):
        """Scrolls down the payment options index tree and clicks the parent list item container."""
        self.log.info("Loading payment options view pane context...")
        time.sleep(6)

        try:
            self.log.info("Locating the Credit & Debit Cards <li> container...")
            card_tab_el = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.CREDIT_DEBIT_CARD_TAB)
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_tab_el)
            time.sleep(2)

            # Click the container directly using Javascript
            self.log.info("Executing Javascript click on the payment tab container...")
            self.driver.execute_script("arguments[0].click();", card_tab_el)

            # Wait for the card entry form to drop down and render
            time.sleep(4)

        except Exception as e:
            self.log.error(f"Failed to click the card payment tab container: {str(e)}")
            raise e

    def input_card_credentials_from_csv(self, data_set):
        """Waits explicitly for each field to be visible, then enters CSV data."""
        self.log.info("Waiting for Card Input fields to become visible...")

        try:
            # 1. Wait for and fill Card Number
            num_field = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)
            )
            num_field.clear()
            num_field.send_keys(data_set['card_number'])
            self.log.info("CSV READ: Injected Card Number.")

            # 2. Wait for and fill Name on Card (This is where it crashed last time!)
            name_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.CARD_NAME_INPUT)
            )
            name_field.clear()
            name_field.send_keys(data_set['card_name'])
            self.log.info("CSV READ: Injected Card Name.")

            # 3. Expiry Month and Year
            exp_m_field = self.driver.find_element(*self.EXPIRY_MONTH_SELECT)
            exp_m_field.send_keys(data_set['expiry_month'])

            exp_y_field = self.driver.find_element(*self.EXPIRY_YEAR_SELECT)
            exp_y_field.send_keys(data_set['expiry_year'])

            # 4. CVV Verification Code
            cvv_field = self.driver.find_element(*self.CVV_INPUT)
            cvv_field.clear()
            cvv_field.send_keys(data_set['cvv_code'])
            self.log.info("CSV READ: Injected CVV verification string successfully.")

            time.sleep(3)
            self.log.info("Payment details successfully entered from CSV!")

        except Exception as e:
            self.log.error(f"Error entering payment credentials: {str(e)}")
            raise e