Feature: Hotel Booking Validation Suite

  Background:
    Given I navigate to the MakeMyTrip homepage

  @positive @critical
  Scenario Outline: Positive Booking Flow - <test_scenario>
    When I dismiss the login popup and click on the hotels module
    And I search for the hotel destination "<destination>"
    And I trigger the search query
    And I apply the 5-star filter on the results page
    And I select the first hotel and click Book Now
    And I fill guest details from CSV row "<csv_row>"
    And I handle secure trip and continue
    Then the system should transition to the payment gateway

    Examples:
      | test_scenario               | destination | csv_row |
      | Positive_Standard_Booking_1 | Hyderabad   | 1       |
      | Positive_Standard_Booking_2 | Bangalore   | 2       |

  @negative @normal
  Scenario Outline: Negative Validation Flow - <test_scenario>
    When I dismiss the login popup and click on the hotels module
    And I search for the hotel destination "<destination>"
    And I trigger the search query
    And I apply the 5-star filter on the results page
    And I select the first hotel and click Book Now
    And I submit the form with invalid or missing data for "<test_scenario>"
    Then the system should enforce validation rules based on "<test_scenario>"

    Examples:
      | test_scenario              | destination |
      | Negative_Missing_FirstName | Hyderabad   |
      | Negative_Missing_Email     | Bangalore   |