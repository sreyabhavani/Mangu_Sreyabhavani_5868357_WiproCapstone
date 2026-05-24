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
    context.driver.get("https://www.makemytrip.com/")
    time.sleep(3)
    assert "MakeMyTrip" in context.driver.title, f"Expected 'MakeMyTrip' in title, but got '{context.driver.title}'"


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
    time.sleep(8)  # Allow initial search results to render completely


# --- PHASE 2: SEARCH RESULTS & FILTERS ---

@when('I apply the 5-star filter on the results page')
def step_impl(context):
    details_page = HotelDetailsPage(context.driver)
    details_page.apply_5_star_filter()
    time.sleep(5)  # Crucial: Allow lazy loading grid to update after filter application


@when('I select the first hotel and click Book Now')
def step_impl(context):
    # Dynamic recovery layer for lazy-loaded element selectors
    try:
        # Pre-scroll window layout context to initialize elements down the grid
        context.driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)

        details_page = HotelDetailsPage(context.driver)
        details_page.select_first_hotel()
        time.sleep(3)
        details_page.click_book_now_on_details_page()
    except Exception as ex:
        # Fallback handling selector directly if DOM wrapper shifts properties dynamically
        print(f"Primary DOM path blocked. Triggering structural fallbacks... Error: {str(ex)}")

        # Shift handles to handle new browser tabs if opened automatically
        if len(context.driver.window_handles) > 1:
            context.driver.switch_to.window(context.driver.window_handles[-1])

        details_page = HotelDetailsPage(context.driver)
        details_page.click_book_now_on_details_page()


# --- PHASE 3: REVIEW PAGE & DATA ENTRY ---

# --- PHASE 3: REVIEW PAGE & DATA ENTRY ---

@when('I fill guest details from legacy guest_date.csv row')
def step_impl(context):
    raw_data = CsvReader.get_test_data("data/guest_date.csv", "1")

    if not raw_data:
        raise ValueError("No data rows could be read from data/guest_date.csv")

    data_set = raw_data.copy()

    # Mapping the data safely
    data_set['firstName'] = data_set.get('firstName', data_set.get('firstName'))
    data_set['first_name'] = data_set.get('firstName')

    data_set['lastName'] = data_set.get('lastName', data_set.get('lastName'))
    data_set['last_name'] = data_set.get('lastName')

    data_set['mobileNumber'] = data_set.get('mobileNumber', data_set.get('mobileNumber'))
    data_set['mobile'] = data_set.get('mobileNumber')

    data_set['panNumber'] = data_set.get('panNumber', data_set.get('panNumber'))
    data_set['pan_number'] = data_set.get('panNumber')

    data_set['email'] = data_set.get('email', '')

    booking_page = BookingPage(context.driver)

    # FIX: Changed from fill_guest_details_from_csv() to match your actual POM method name
    booking_page.fill_guest_details(data_set)


@when('I handle secure trip options and continue to payment')
def step_impl(context):
    # Updated text registration string matches feature layout targets perfectly
    booking_page = BookingPage(context.driver)
    booking_page.handle_secure_trip_and_continue()


# --- PHASE 4: GATEWAY TRANSITION VERIFICATION ---

@then('the system should transition to the payment gateway and capture an Allure screenshot')
def step_impl(context):
    time.sleep(15)  # Retain browser visualization status exactly as coded

    current_url = context.driver.current_url
    assert "hotel-review" not in current_url or "checkout" in current_url or "payment" in current_url, \
        f"Failed to transition outside hotel review space. Landing page URL: {current_url}"

    allure.attach(
        context.driver.get_screenshot_as_png(),
        name="Final_Gateway_State_Verification",
        attachment_type=allure.attachment_type.PNG
    )


#
# # --- POSITIVE FLOW STEPS ---
#
# @when('I fill guest details from CSV row "{csv_row}"')
# def step_impl(context, csv_row):
#     # Fetch data based on row index
#     data_set = CsvReader.get_test_data("data/test_case.csv", csv_row)
#     if not data_set:
#         raise ValueError(f"Could not read row {csv_row} from CSV.")
#
#     booking_page = BookingPage(context.driver)
#     booking_page.fill_guest_details(data_set)
#
#
# @when('I handle secure trip and continue')
# def step_impl(context):
#     booking_page = BookingPage(context.driver)
#     booking_page.handle_secure_trip_and_continue()
#
#
# @then('the system should transition to the payment gateway')
# def step_impl(context):
#     time.sleep(8)  # Wait for transition processing
#     current_url = context.driver.current_url
#     assert "hotel-review" not in current_url or "checkout" in current_url, \
#         f"Transition failed. User stuck on URL: {current_url}"
#
#
# # --- NEGATIVE FLOW STEPS ---
#
# @when('I submit the form with invalid or missing data for "{test_scenario}"')
# def step_impl(context, test_scenario):
#     # Fetch negative dataset based on scenario name rather than index
#     data_set = CsvReader.get_data_by_scenario("data/test_case.csv", test_scenario)
#
#     booking_page = BookingPage(context.driver)
#     booking_page.fill_guest_details(data_set)
#     booking_page.handle_secure_trip_and_continue()
#     time.sleep(3)  # Give UI time to trigger validation flags
#
#
# @then('the system should enforce validation rules based on "{test_scenario}"')
# def step_impl(context, test_scenario):
#     booking_page = BookingPage(context.driver)
#
#     if test_scenario == "Negative_Missing_FirstName":
#         # Verifies the specific UI text block
#         booking_page.verify_validation_message("Please enter guest's first name")
#
#     elif test_scenario == "Negative_Invalid_PAN_Format":
#         # Verifies the user is blocked from moving forward
#         booking_page.verify_on_page("hotel-review")
