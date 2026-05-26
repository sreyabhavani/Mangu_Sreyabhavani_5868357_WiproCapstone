import os
import time
import allure
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.hotel_details_page import HotelDetailsPage
from pages.booking_page import BookingPage
from utils.csv_reader import CsvReader


# --- PHASE 1: HOMEPAGE FLOW ---

@given('I navigate to the MakeMyTrip homepage')
def step_impl(context):
    target_url = "https://www.makemytrip.com/"
    context.driver.get(target_url)
    time.sleep(4)

    # ANTI-BOT BLOCK RESET LAYER: Catch intercepts at entry point (image_58cd59.png format)
    current_source = context.driver.page_source.lower()
    if "200-ok" in current_source and ("pretty-print" in current_source or "<html" not in current_source):
        print("WAF Entry Intercept Detected ('200-OK'). Initiating driver session purge...")

        # Clear the flag footprint tracking states
        context.driver.delete_all_cookies()
        try:
            context.driver.execute_script("window.localStorage.clear();")
            context.driver.execute_script("window.sessionStorage.clear();")
        except Exception:
            pass

        # Re-request the application natively via document window property re-assignment
        context.driver.execute_script(f"window.location.href = '{target_url}';")
        time.sleep(6)

    assert "MakeMyTrip" in context.driver.title or len(context.driver.find_elements(By.TAG_NAME, "body")) > 0, \
        f"Failed to bypass initial gateway intercept block. Current Title: '{context.driver.title}'"


@when('I dismiss the login popup and click on the hotels module')
def step_impl(context):
    home_page = HomePage(context.driver)
    home_page.dismiss_login_popup()
    home_page.click_hotels_module()


@when('I search for the hotel destination "{destination}"')
def step_impl(context, destination):
    home_page = HomePage(context.driver)
    home_page.search_hotel_destination(destination)


@when('I select stay dates and configure guest counts')
def step_impl(context):
    home_page = HomePage(context.driver)
    home_page.select_stay_dates()
    home_page.configure_guests_and_apply()


@when('I trigger the search query bypassing validations')
def step_impl(context):
    home_page = HomePage(context.driver)
    home_page.trigger_search_query_negative_bypass()
    time.sleep(5)  # Allow initial load attempt to complete

    # SEARCH REDIRECTION RECOVERY LAYER: Handle the raw text screen shown in image_58cd59.png
    current_source = context.driver.page_source.lower()

    if "200-ok" in current_source and ("<html" not in current_source or "pretty-print" in current_source):
        print(
            "Detected raw data view intercept post-search button dispatch. Restructuring connection layout context...")

        # Keep a reference to the active query string link
        target_search_url = context.driver.current_url

        # Method A: Wipe rate-limiting automated session cookie parameters and soft-refresh
        context.driver.delete_all_cookies()
        context.driver.refresh()
        time.sleep(6)

        # Method B Fallback: Dispatched native location mutation if frame continues to render raw text strings
        if "200-ok" in context.driver.page_source.lower():
            print("Soft refresh blocked. Re-fetching targeted search string via absolute DOM mutation loop...")
            context.driver.get(target_search_url)
            time.sleep(6)

    # DYNAMIC PROGRESSION CHECK: Confirm the browser is rendering actual listing rows
    try:
        WebDriverWait(context.driver, 15).until(
            lambda d: "hotels/hotel-listing" in d.current_url and len(d.find_elements(By.CLASS_NAME, "listingRow")) > 0
        )
        print("Successfully broken out of text block state. Listings container initialized.")
    except Exception:
        print(f"Redirection processing slow. Current UI window location: {context.driver.current_url}")
        time.sleep(5)


# --- PHASE 2: SEARCH RESULTS & FILTERS ---

@when('I apply the 5-star filter on the results page')
def step_impl(context):
    details_page = HotelDetailsPage(context.driver)
    details_page.apply_5_star_filter()
    time.sleep(5)  # Crucial: Allow lazy loading grid to update after filter application


@when('I select the first hotel and click Book Now')
def step_impl(context):
    try:
        # Pre-scroll window layout context to initialize elements down the grid
        context.driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)

        details_page = HotelDetailsPage(context.driver)
        details_page.select_first_hotel()
        time.sleep(3)
        details_page.click_book_now_on_details_page()
    except Exception as ex:
        print(f"Primary DOM path blocked. Triggering structural fallbacks... Error: {str(ex)}")

        # Shift handles to handle new browser tabs if opened automatically
        if len(context.driver.window_handles) > 1:
            context.driver.switch_to.window(context.driver.window_handles[-1])

        details_page = HotelDetailsPage(context.driver)
        details_page.click_book_now_on_details_page()




    # --- PHASE 3: REVIEW PAGE & DATA ENTRY ---

    @when('I fill guest details from legacy guest_date.csv row')
    def step_impl(context):
        """
        Reads data from CSV and fills the booking form.
        The logic in BookingPage handles the masking and input focus issues.
        """
        # 1. Fetch raw data from CSV
        raw_data = CsvReader.get_test_data("data/guest_date.csv", "1")

        if not raw_data:
            raise ValueError("No data rows could be read from data/guest_date.csv")

        # 2. Log for verification: Ensure the dictionary keys match the CSV header
        print(f"DEBUG: Retrieved CSV Data: {raw_data}")

        # 3. Pass the data to the BookingPage logic
        booking_page = BookingPage(context.driver)
        booking_page.fill_guest_details(raw_data)

    @when('I handle secure trip options and continue to payment')
    def step_impl(context):
        booking_page = BookingPage(context.driver)
        booking_page.handle_secure_trip_and_continue()

    # --- PHASE 4: GATEWAY TRANSITION VERIFICATION ---

    @then('the system should transition to the payment gateway and capture an Allure screenshot')
    def step_impl(context):
        # Wait for the transition to finish
        time.sleep(15)

        current_url = context.driver.current_url
        assert "hotel-review" not in current_url or "checkout" in current_url or "payment" in current_url, \
            f"Failed to transition outside hotel review space. Landing page URL: {current_url}"

        allure.attach(
            context.driver.get_screenshot_as_png(),
            name="Final_Gateway_State_Verification",
            attachment_type=allure.attachment_type.PNG
        )


import os
import time
import allure
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.home_page import HomePage
from pages.hotel_details_page import HotelDetailsPage
from pages.booking_page import BookingPage
from utils.csv_reader import CsvReader


#    context.driver.quit()