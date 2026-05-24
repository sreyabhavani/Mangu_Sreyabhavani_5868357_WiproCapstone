import os
import time
import pytest
import allure
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.hotel_details_page import HotelDetailsPage
from pages.booking_page import BookingPage
from utils.csv_reader import CSVReader
from utils.logger import AutomationLogger


@allure.suite("Hotel Booking Validation Suite")
class TestBookingValidationSuite:
    log = AutomationLogger.get_logger("TestBookingValidationSuite")

    def load_target_url(self):
        return "https://www.makemytrip.com/"

    # =================================================================================
    # 👍 POSITIVE RUNS
    # =================================================================================
    @allure.title("Positive Booking Flow: {data_set[test_scenario]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data_set",
                             [row for row in CSVReader.read_csv("guest_test.csv") if "Positive" in row['test_scenario']])
    def test_positive_booking_flow(self, driver, data_set):
        self.log.info(f"--- POSITIVE RUN: Processing {data_set.get('first_name')} ---")

        with allure.step("Navigate to MakeMyTrip Home Page"):
            driver.get(self.load_target_url())
            home_page = HomePage(driver)
            home_page.dismiss_login_popup()

        with allure.step("Search for Hotels"):
            home_page.click_hotels_module()
            home_page.search_hotel_destination(data_set['destination'])
            home_page.select_stay_dates()
            home_page.configure_guests_and_apply()
            home_page.trigger_search_query_negative_bypass()
            time.sleep(6)

        with allure.step("Select 5-Star Hotel"):
            details_page = HotelDetailsPage(driver)
            details_page.apply_5_star_filter()
            details_page.select_first_hotel()
            details_page.click_book_now_on_details_page()

        with allure.step("Fill Guest Details and Continue"):
            booking_page = BookingPage(driver)
            booking_page.fill_guest_details_from_csv(data_set)
            booking_page.handle_secure_trip_and_continue()
            time.sleep(8)

        with allure.step("Verify Successful Transition to Checkout"):
            post_click_url = driver.current_url

            # Attach screenshot before assertion for reference
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Checkout_Attempt_{data_set['test_scenario']}",
                attachment_type=allure.attachment_type.PNG
            )

            assert "hotel-review" not in post_click_url or "checkout" in post_click_url, "Failed to transition to checkout."
            self.log.info("Assertion Passed! Saved verification screenshot via Allure.")

    # =================================================================================
    # 👎 NEGATIVE RUNS
    # =================================================================================
    @allure.title("Negative Validation Flow: {data_set[test_scenario]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("data_set",
                             [row for row in CSVReader.read_csv("guest_test.csv") if "Negative" in row['test_scenario']])
    def test_negative_validation_flows(self, driver, data_set):
        self.log.info(f"--- RUNNING NEGATIVE TESTING DATASET: {data_set['test_scenario']} ---")

        with allure.step("Navigate to MakeMyTrip Home Page"):
            driver.get(self.load_target_url())
            home_page = HomePage(driver)
            home_page.dismiss_login_popup()

        with allure.step("Search for Hotels"):
            home_page.click_hotels_module()
            home_page.search_hotel_destination(data_set['destination'])
            home_page.select_stay_dates()
            home_page.configure_guests_and_apply()
            home_page.trigger_search_query_negative_bypass()
            time.sleep(6)

        with allure.step("Select 5-Star Hotel"):
            details_page = HotelDetailsPage(driver)
            details_page.apply_5_star_filter()
            details_page.select_first_hotel()
            details_page.click_book_now_on_details_page()

        with allure.step("Submit Form with Invalid/Missing Data"):
            booking_page = BookingPage(driver)
            booking_page.fill_guest_details_from_csv(data_set)
            booking_page.handle_secure_trip_and_continue()
            time.sleep(3)

        with allure.step("Verify Form Error Elements and URL States"):
            # Attach screenshot of the page state before assertions run
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Validation_State_{data_set['test_scenario']}",
                attachment_type=allure.attachment_type.PNG
            )

            if data_set['test_scenario'] == "Negative_Missing_FirstName":
                validation_error_msgs = driver.find_elements(By.XPATH,
                                                             "//*[contains(text(), \"Please enter guest's first name\")]")
                assert len(validation_error_msgs) > 0, "Form allowed submission despite an empty first name field!"
                self.log.info("Negative check successful: Blocker text found on screen.")

            elif data_set['test_scenario'] == "Negative_Invalid_PAN_Format":
                ending_url = driver.current_url
                assert "hotel-review" in ending_url, f"System bypassed error gates with an invalid PAN string format!"
                self.log.info("Negative check successful: User stayed safely locked on review page.")