import os
import time
import pytest
from pages.home_page import HomePage
from pages.hotel_details_page import HotelDetailsPage
from pages.booking_page import BookingPage
from utils.csv_reader import CSVReader
from utils.logger import AutomationLogger


class TestMakeMyTrip:
    log = AutomationLogger.get_logger("TestMakeMyTrip")

    def load_target_url(self):
        return "https://www.makemytrip.com/"

    @pytest.mark.parametrize("data_set", CSVReader.read_csv("get_test.csv"))
    def test_navigate_to_hotels_module(self, driver, data_set):
        self.log.info("======================= STARTING PHASE 1 HOMEPAGE FLOW =======================")
        target_url = self.load_target_url()

        driver.get(target_url)
        home_page = HomePage(driver)

        # 1. Search Query Inputs
        home_page.dismiss_login_popup()
        home_page.click_hotels_module()
        home_page.search_hotel_destination(data_set['destination'])
        home_page.select_stay_dates()
        home_page.configure_guests_and_apply()

        # 2. Grid Result Navigation
        home_page.trigger_search_query_negative_bypass()
        time.sleep(6)

        self.log.info("======================= STARTING PHASE 2 FILTER & BOOKING FLOW =======================")
        details_page = HotelDetailsPage(driver)
        details_page.apply_5_star_filter()
        details_page.select_first_hotel()
        details_page.click_book_now_on_details_page()

        self.log.info("======================= STARTING PHASE 3 BOOKING PAGE DATA ENTRY =======================")
        booking_page = BookingPage(driver)

        # Enters user data AND newly tracked PAN options from your CSV rows
        booking_page.fill_guest_details_from_csv(data_set)

        # Selects 'Yes, secure my trip.' and clicks PAY NOW
        booking_page.handle_secure_trip_and_continue()

        # =================================================================================
        # 🛑 INTENTIONAL STOP POINT: PHASE 4 PAYMENT OPTION SELECTION REMOVED BELOW
        # =================================================================================
        self.log.info("======================= GATEWAY TRANSITION VERIFICATION =======================")
        self.log.info("Successfully clicked PAY NOW. Holding browser open for visual verification...")

        # Keep the browser alive for 15 seconds so you can watch the landing gateway
        time.sleep(15)

        self.log.info("======================= AUTOMATION RUN CONCLUDED SUCCESSFUL =======================")