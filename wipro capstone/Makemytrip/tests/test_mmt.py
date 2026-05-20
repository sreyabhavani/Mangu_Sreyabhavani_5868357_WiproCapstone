import os
import time
from pages.home_page import HomePage


class TestMakeMyTrip:

    def load_target_url(self):
        """Fetches active config path declarations with a reliable fallback route option."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        possible_paths = [
            os.path.join(base_dir, "config.properties"),
            os.path.join(base_dir, "tests", "config.properties"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.properties")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as file:
                        for line in file:
                            line = line.strip()
                            if line and line.startswith("url="):
                                return line.split("=", 1)[1].strip()
                except:
                    pass
        return "https://www.makemytrip.com/"

    def test_navigate_to_hotels_module(self, driver):
        # 1. Environment Build Injection
        target_url = self.load_target_url()
        driver.get(target_url)
        home_page = HomePage(driver)

        # 2. Sequential Dashboard Interaction Workflows [Image 1, 2]
        home_page.dismiss_login_popup()
        home_page.click_hotels_module()
        home_page.search_hotel_destination("Goa")
        home_page.select_stay_dates()

        # 3. Form Dispatch Execution Handling [Image 4 Fix Applied]
        home_page.trigger_search_query()

        # 4. Result Matrix Filtering and Focus Selection [Image 3]
        home_page.apply_filters()

        # 5. Extract Item Card Target Choice
        home_page.select_first_hotel()

        # 6. Shift Execution Focus Space to New Tab Context Window Safely
        window_handles = driver.window_handles
        if len(window_handles) > 1:
            print(
                "[INFO] Moving automation engine session context profile over onto the item details view panel tab...")
            driver.switch_to.window(window_handles[1])

        print(
            f"[SUCCESS] Test Completed. Browser focused page endpoint path context destination reads: {driver.current_url}")
        assert len(window_handles) > 1 or "detail" in driver.current_url.lower()