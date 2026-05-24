from selenium.webdriver.common.by import By

class HotelDetailsPageLocators:
    POPUP_SKIP_BUTTON = (By.XPATH, "//span[text()='SKIP' or text()='Skip'] | //p[text()='SKIP']")
    FIVE_STAR_FILTERS = [
        (By.XPATH, "//span[text()='5 Star']"),
        (By.XPATH, "//label[contains(., '5 Star')]"),
        (By.XPATH, "//label[contains(@for, '5')]")
    ]
    EXACT_HOTEL_LINK = (By.XPATH, "//div[@id='Listing_hotel_0']//a | //div[@id='Listing_hotel_0']/a")
    FALLBACK_HOTEL_LINK = (By.XPATH, "(//a[contains(@href, 'hotel-details')])[1]")
    BOOK_NOW_LOCATORS = [
        (By.XPATH, "//button[contains(., 'BOOK THIS NOW')]"),
        (By.XPATH, "//a[contains(., 'BOOK THIS NOW')]"),
        (By.XPATH, "//*[contains(text(), 'BOOK THIS NOW')]"),
        (By.XPATH, "//button[text()='BOOK NOW' or text()='Book Now']")
    ]