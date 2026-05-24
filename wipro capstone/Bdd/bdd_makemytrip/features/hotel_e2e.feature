Feature: MakeMyTrip Hotel Booking Core Suite
  As an automation framework user,
  I want to run complete end-to-end hotel booking flows,
  So that I can verify search, selection, data entry, and payment gateway redirection.

  @CRITICAL @E2E
  Scenario: Hotel Booking End-to-End Flow using Single Guest Dataset
    # PHASE 1: HOMEPAGE FLOW
    Given I navigate to the MakeMyTrip homepage
    When I dismiss the login popup and click on the hotels module
    And I search for the hotel destination "Bali"
    And I select stay dates and configure guest counts
    And I trigger the search query bypassing validations

    # PHASE 2: SEARCH RESULTS & FILTERS
    And I apply the 5-star filter on the results page
    And I select the first hotel and click Book Now

    # PHASE 3: REVIEW PAGE & DATA ENTRY
    And I fill guest details from legacy guest_date.csv row
    And I handle secure trip options and continue to payment

    # PHASE 4: GATEWAY TRANSITION VERIFICATION
    Then the system should transition to the payment gateway and capture an Allure screenshot