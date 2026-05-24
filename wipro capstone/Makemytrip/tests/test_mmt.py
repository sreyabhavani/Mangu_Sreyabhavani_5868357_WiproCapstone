import os
import time
import pytest
import allure
from pages.home_page import HomePage
from pages.hotel_details_page import HotelDetailsPage
from pages.booking_page import BookingPage
from utils.csv_reader import CSVReader
from utils.logger import AutomationLogger

@allure.suite("MakeMyTrip Hotel Booking Core Suite")
class TestMakeMyTrip:
    log = AutomationLogger.get_logger("TestMakeMyTrip")

    def load_target_url(self):
        return "https://www.makemytrip.com/"

    @allure.title("Hotel Booking End-to-End Flow: {data_set[test_scenario]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data_set", CSVReader.read_csv("get_test.csv"))
    def test_navigate_to_hotels_module(self, driver, data_set):
        # -----------------------------------------------------------------------------
        # PHASE 1: HOMEPAGE FLOW
        # -----------------------------------------------------------------------------
        self.log.info("======================= STARTING PHASE 1 HOMEPAGE FLOW =======================")
        target_url = self.load_target_url()

        with allure.step("Navigate to Home Page and Fill Search Criteria"):
            driver.get(target_url)
            home_page = HomePage(driver)

            # 1. Search Query Inputs
            home_page.dismiss_login_popup()
            home_page.click_hotels_module()
            home_page.search_hotel_destination(data_set['destination'])
            home_page.select_stay_dates()
            home_page.configure_guests_and_apply()

        with allure.step("Trigger Search Query"):
            # 2. Grid Result Navigation
            home_page.trigger_search_query_negative_bypass()
            time.sleep(6)

        # -----------------------------------------------------------------------------
        # PHASE 2: FILTER & BOOKING FLOW
        # -----------------------------------------------------------------------------
        self.log.info("======================= STARTING PHASE 2 FILTER & BOOKING FLOW =======================")

        with allure.step("Filter by 5-Star and Select First Hotel"):
            details_page = HotelDetailsPage(driver)
            details_page.apply_5_star_filter()
            details_page.select_first_hotel()
            details_page.click_book_now_on_details_page()

        # -----------------------------------------------------------------------------
        # PHASE 3: BOOKING PAGE DATA ENTRY
        # -----------------------------------------------------------------------------
        self.log.info("======================= STARTING PHASE 3 BOOKING PAGE DATA ENTRY =======================")
        booking_page = BookingPage(driver)

        with allure.step("Fill Guest Info & Submit Booking"):
            # Enters user data AND newly tracked PAN options from your CSV rows
            booking_page.fill_guest_details_from_csv(data_set)

            # Selects 'Yes, secure my trip.' and clicks PAY NOW
            booking_page.handle_secure_trip_and_continue()

        # -----------------------------------------------------------------------------
        # PHASE 4: GATEWAY TRANSITION VERIFICATION
        # -----------------------------------------------------------------------------
        self.log.info("======================= GATEWAY TRANSITION VERIFICATION =======================")
        self.log.info("Successfully clicked PAY NOW. Holding browser open for visual verification...")

        with allure.step("Hold Gateway Transition and Capture Verification Screenshot"):
            # Keep the browser alive for 15 seconds so you can watch the landing gateway
            time.sleep(15)

            # Capture and attach the final page view directly into the Allure report step
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Final_Gateway_State_{data_set['test_scenario']}",
                attachment_type=allure.attachment_type.PNG
            )

        self.log.info("======================= AUTOMATION RUN CONCLUDED SUCCESSFUL =======================")