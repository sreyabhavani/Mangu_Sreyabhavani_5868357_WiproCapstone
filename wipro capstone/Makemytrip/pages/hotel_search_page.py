from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HotelSearchPage(BasePage):
    # Selectors extracted from DOM snapshot db1b30da
    CITY_INPUT_TRIGGER = (By.XPATH, "//div[@data-cy='HotelSearchWidget_316']//label[@for='city']")
    CITY_INPUT_FIELD = (By.XPATH, "//input[@data-cy='city' and @id='city']")
    CITY_SUGGESTION_GOA = (By.XPATH,
                           "//ul[contains(@class, 'react-autosuggest__suggestions-list')]//li[contains(., 'Goa')]")

    # Target values exactly matching target dates: 27th May 2026 to 30th May 2026
    CHECK_IN_DATE = (By.XPATH, "//div[@aria-label='Wed May 27 2026' or contains(@class, 'day') and contains(., '27')]")
    CHECK_OUT_DATE = (By.XPATH, "//div[@aria-label='Sat May 30 2026' or contains(@class, 'day') and contains(., '30')]")

    ROOMS_GUESTS_SELECTOR = (By.XPATH, "//div[@data-cy='HotelSearchWidget_319']//label[@for='guest']")
    ADULTS_COUNT_2 = (By.XPATH, "//li[@data-cy='adults-2'] | //span[text()='2']")
    APPLY_GUEST_BTN = (By.XPATH, "//button[@data-cy='submitGuest' or contains(@class, 'btnApply')]")
    SEARCH_BTN = (By.XPATH, "//button[@id='hsw_search_button' or @data-cy='submit']")

    def search_hotels_goa(self):
        self.click_element(self.CITY_INPUT_TRIGGER)
        self.send_keys_to_element(self.CITY_INPUT_FIELD, "Goa")
        self.click_element(self.CITY_SUGGESTION_GOA)
        self.click_element(self.CHECK_IN_DATE)
        self.click_element(self.CHECK_OUT_DATE)
        self.click_element(self.ROOMS_GUESTS_SELECTOR)
        self.click_element(self.ADULTS_COUNT_2)
        self.click_element(self.APPLY_GUEST_BTN)
        self.click_element(self.SEARCH_BTN)