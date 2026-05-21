import os
import time
import pytest
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.hotel_details_page import HotelDetailsPage
from pages.booking_page import BookingPage
from utils.csv_reader import CSVReader
from utils.logger import AutomationLogger


class TestBookingValidationSuite:
    log = AutomationLogger.get_logger("TestBookingValidationSuite")

    def load_target_url(self):
        return "https://www.makemytrip.com/"

    # =================================================================================
    # 👍 POSITIVE RUNS (Captures explicit confirmation images)
    # =================================================================================
    @pytest.mark.parametrize("data_set",
                             [row for row in CSVReader.read_csv("get_test.csv") if "Positive" in row['test_scenario']])
    def test_positive_booking_flow(self, driver, data_set):
        self.log.info(f"--- POSITIVE RUN: Processing {data_set.get('first_name')} ---")

        driver.get(self.load_target_url())
        home_page = HomePage(driver)
        home_page.dismiss_login_popup()
        home_page.click_hotels_module()
        home_page.search_hotel_destination(data_set['destination'])
        home_page.select_stay_dates()
        home_page.configure_guests_and_apply()
        home_page.trigger_search_query_negative_bypass()
        time.sleep(6)

        details_page = HotelDetailsPage(driver)
        details_page.apply_5_star_filter()
        details_page.select_first_hotel()
        details_page.click_book_now_on_details_page()

        booking_page = BookingPage(driver)
        booking_page.fill_guest_details_from_csv(data_set)
        booking_page.handle_secure_trip_and_continue()
        time.sleep(8)

        # Assertion Check
        post_click_url = driver.current_url
        assert "hotel-review" not in post_click_url or "checkout" in post_click_url, "Failed to transition to checkout."

        # SUCCESS CAPTURE: Explicitly snap a photo showing the test passed successfully!
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(f"screenshots/PASSED_{data_set['test_scenario']}.png")
        self.log.info("Assertion Passed! Saved verification screenshot.")

    # =================================================================================
    # 👎 NEGATIVE RUNS (Relies on the conftest wrapper for automatic snaps on failure)
    # =================================================================================
    @pytest.mark.parametrize("data_set",
                             [row for row in CSVReader.read_csv("get_test.csv") if "Negative" in row['test_scenario']])
    def test_negative_validation_flows(self, driver, data_set):
        self.log.info(f"--- RUNNING NEGATIVE TESTING DATASET: {data_set['test_scenario']} ---")

        driver.get(self.load_target_url())
        home_page = HomePage(driver)
        home_page.dismiss_login_popup()
        home_page.click_hotels_module()
        home_page.search_hotel_destination(data_set['destination'])
        home_page.select_stay_dates()
        home_page.configure_guests_and_apply()
        home_page.trigger_search_query_negative_bypass()
        time.sleep(6)

        details_page = HotelDetailsPage(driver)
        details_page.apply_5_star_filter()
        details_page.select_first_hotel()
        details_page.click_book_now_on_details_page()

        booking_page = BookingPage(driver)
        booking_page.fill_guest_details_from_csv(data_set)
        booking_page.handle_secure_trip_and_continue()
        time.sleep(3)

        # Dynamic validation parsing based on the row objective
        if data_set['test_scenario'] == "Negative_Missing_FirstName":
            validation_error_msgs = driver.find_elements(By.XPATH,
                                                         "//*[contains(text(), \"Please enter guest's first name\")]")

            # If this assertion fails (meaning len == 0), conftest.py instantly saves a screenshot
            assert len(validation_error_msgs) > 0, "Form allowed submission despite an empty first name field!"

            # If it passes, save a manual proof snapshot
            driver.save_screenshot(f"screenshots/PASSED_{data_set['test_scenario']}.png")
            self.log.info("Negative check successful: Blocker text found on screen.")

        elif data_set['test_scenario'] == "Negative_Invalid_PAN_Format":
            ending_url = driver.current_url

            # If this assertion fails, conftest.py instantly saves a screenshot
            assert "hotel-review" in ending_url, f"System bypassed error gates with an invalid PAN string format!"

            driver.save_screenshot(f"screenshots/PASSED_{data_set['test_scenario']}.png")
            self.log.info("Negative check successful: User stayed safely locked on review page.")