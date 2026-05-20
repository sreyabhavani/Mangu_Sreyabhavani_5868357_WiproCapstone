from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HotelDetailsPage(BasePage):
    # Captured exactly from snapshot 1000362260
    BOOK_NOW_BTN = (By.XPATH, "//button[contains(text(), 'BOOK NOW') or @id='detpg_book_combo_btn']")

    def proceed_to_booking(self):
        self.click_element(self.BOOK_NOW_BTN)