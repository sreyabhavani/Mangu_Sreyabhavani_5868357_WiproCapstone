from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class BookingPage(BasePage):
    # Mapped from DOM fields 854d4207, 4d18f15c, 5c0b48ed, 37c0e88a, 9999f0c7, a830fd5b, df8ca7a5, 83d099a2
    BREAKFAST_ADDON_CHECKBOX = (By.XPATH,
                                "//span[contains(., 'Breakfast')]//preceding-sibling::input | //div[contains(text(), 'Breakfast')]")

    FIRST_NAME_INPUT = (By.XPATH, "//input[@id='fName']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@id='lName']")
    MOBILE_INPUT = (By.XPATH, "//input[@id='mNo']")
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")

    CREDIT_DEBIT_CARD_OPTION = (By.XPATH,
                                "//p[@data-testid='paymode-title' and contains(text(), 'Credit & Debit Cards')]")
    CARD_NUMBER_INPUT = (By.XPATH, "//input[@id='cardNumber']")
    CARD_NAME_INPUT = (By.XPATH, "//input[@id='cardName' or @id='nameOnCard']")
    CARD_EXPIRY_MONTH = (By.XPATH, "//input[@id='expiryMonth']")
    CARD_EXPIRY_YEAR = (By.XPATH, "//input[@id='expiryYear']")
    CARD_CVV_INPUT = (By.XPATH, "//input[@id='cardCvv']")

    def add_breakfast(self):
        try:
            self.click_element(self.BREAKFAST_ADDON_CHECKBOX)
        except Exception:
            pass

    def fill_guest_details(self, first_name, last_name, mobile, email):
        self.send_keys_to_element(self.FIRST_NAME_INPUT, first_name)
        self.send_keys_to_element(self.LAST_NAME_INPUT, last_name)
        self.send_keys_to_element(self.MOBILE_INPUT, mobile)
        self.send_keys_to_element(self.EMAIL_INPUT, email)

    def fill_payment_details(self, card_no, card_name, exp_month, exp_year, cvv):
        self.click_element(self.CREDIT_DEBIT_CARD_OPTION)
        self.send_keys_to_element(self.CARD_NUMBER_INPUT, card_no)
        self.send_keys_to_element(self.CARD_NAME_INPUT, card_name)
        self.send_keys_to_element(self.CARD_EXPIRY_MONTH, str(exp_month))
        self.send_keys_to_element(self.CARD_EXPIRY_YEAR, str(exp_year))
        self.send_keys_to_element(self.CARD_CVV_INPUT, str(cvv))