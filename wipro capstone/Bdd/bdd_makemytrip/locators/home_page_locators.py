from selenium.webdriver.common.by import By


class HomePageLocators:
    CLOSE_MODAL_X = (By.XPATH, "//span[@data-cy='closeModal']")
    LANDING_CONTAINER = (By.XPATH, "//div[@data-cy='landingContainer']")
    HOTELS_MODULE = (By.XPATH, "//li[@data-cy='menu_Hotels']")
    CITY_TAP_CONTAINER = (By.XPATH, "//span[@data-cy='hotelCityLabel']")
    CITY_INPUT_FIELD = (By.XPATH, "//input[@placeholder='Where do you want to stay?']")
    FIRST_SUGGESTION = (By.XPATH, "//ul[contains(@class,'react-autosuggest__suggestions-list')]/li[1]")

    # Dynamic Date Selectors targeting active/selected elements inside the open calendar view
    DYNAMIC_CHECKIN = (By.CSS_SELECTOR, "div.DayPicker-Day[aria-selected='true'], div.DayPicker-Day--today")
    DYNAMIC_CHECKOUT = (By.CSS_SELECTOR,
                        "div.DayPicker-Day[aria-selected='true'] + div.DayPicker-Day, div.DayPicker-Day--today + div.DayPicker-Day")

    GUESTS_APPLY_BUTTON = (By.XPATH, "//button[@data-cy='doneBtn']")
    HOTELS_SEARCH_BUTTON = (By.XPATH, "//button[@data-cy='submit']")
