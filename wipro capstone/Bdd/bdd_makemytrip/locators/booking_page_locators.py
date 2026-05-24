from selenium.webdriver.common.by import By

class BookingPageLocators:
    FIRST_NAME_INPUT = (By.ID, "fName")
    LAST_NAME_INPUT = (By.ID, "lName")
    EMAIL_INPUT = (By.ID, "email")
    MOBILE_INPUT = (By.ID, "mNo")
    PAN_INPUT = (By.XPATH, "//input[@placeholder='ENTER PAN HERE' or contains(@id, 'pan')] | //input[@id='panCheck']")
    SECURE_TRIP_YES_RADIO = (By.XPATH, "//*[contains(text(), 'Yes, secure my trip')] | //label[contains(., 'secure my trip')]")
    CONTINUE_PAYMENT_BUTTON = (By.XPATH, "//a[contains(@class, 'btnContinuePayment')] | //a[contains(text(), 'Pay Now')]")
