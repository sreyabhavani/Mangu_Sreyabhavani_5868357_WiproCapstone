import pytest
import allure
import time
import os

# IMPORT SELENIUMBASE
from seleniumbase import Driver

from utils.logger import AutomationLogger
from utils.screenshot_util import ScreenshotUtil

# FIXED: Now properly calls the get_logger method
logger = AutomationLogger.get_logger("Conftest")


@pytest.fixture()
def driver():
    logger.info("========== STARTING TEST ==========")

    # CREATE DRIVER USING SELENIUMBASE UC MODE
    driver = Driver(uc=True)
    driver.maximize_window()

    # WAITS
    driver.implicitly_wait(5)

    # OPEN WEBSITE
    logger.info("OPENING MAKEMYTRIP WEBSITE")

    driver.get(
        "https://www.makemytrip.com/hotels/"
    )

    # CRITICAL WAF WAIT: Let invisible security scripts resolve
    time.sleep(2)

    logger.info(
        f"CURRENT URL: {driver.current_url}"
    )

    yield driver

    logger.info("========== CLOSING TEST ==========")

    try:

        driver.quit()

        logger.info("BROWSER CLOSED SUCCESSFULLY")

    except Exception as e:

        logger.error(
            f"ERROR CLOSING BROWSER: {str(e)}"
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield

    report = outcome.get_result()

    if report.when == "call":

        if "driver" not in item.funcargs:
            return

        driver = item.funcargs["driver"]

        try:

            if report.passed:

                logger.info(
                    "TEST PASSED - CAPTURING SCREENSHOT"
                )

                path = ScreenshotUtil.capture(
                    driver,
                    f"{item.name}_PASS"
                )

            else:

                logger.error(
                    "TEST FAILED - CAPTURING SCREENSHOT"
                )

                path = ScreenshotUtil.capture(
                    driver,
                    f"{item.name}_FAIL"
                )

            allure.attach.file(
                path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

        except Exception as e:

            logger.error(
                f"SCREENSHOT FAILED: {str(e)}"
            )


def pytest_unconfigure(config):
    import os
    import subprocess

    print("\n===== TESTS COMPLETED - GENERATING ALLURE REPORT =====")

    results_dir = "reports/allure-results"

    # Absolute path to your allure batch file
    allure_path = r"C:\allure\bin\allure.bat"

    if os.path.exists(results_dir) and os.listdir(results_dir):
        if os.path.exists(allure_path):
            print("Launching Allure server...")
            # Wrapping the executable path cleanly in double quotes handles any Windows string parsing bugs
            subprocess.Popen(f'"{allure_path}" serve "{results_dir}"', shell=True)
        else:
            print(f"Error: Allure was not found at {allure_path}. Please check your installation directory.")
    else:
        print(f"Error: The directory '{results_dir}' was not found or is empty.")