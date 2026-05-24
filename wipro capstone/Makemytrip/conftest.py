# import pytest
# import allure
# import time
# import os
#
# # IMPORT SELENIUMBASE
# from seleniumbase import Driver
#
# from utils.logger import AutomationLogger
# from utils.screenshot_util import ScreenshotUtil
#
# # FIXED: Now properly calls the get_logger method
# logger = AutomationLogger.get_logger("Conftest")
#
#
# @pytest.fixture()
# def driver():
#     logger.info("========== STARTING TEST ==========")
#
#     # CREATE DRIVER USING SELENIUMBASE UC MODE
#     driver = Driver(uc=True)
#     driver.maximize_window()
#
#     # WAITS
#     driver.implicitly_wait(5)
#
#     # OPEN WEBSITE
#     logger.info("OPENING MAKEMYTRIP WEBSITE")
#
#     driver.get(
#         "https://www.makemytrip.com/hotels/"
#     )
#
#     # CRITICAL WAF WAIT: Let invisible security scripts resolve
#     time.sleep(2)
#
#     logger.info(
#         f"CURRENT URL: {driver.current_url}"
#     )
#
#     yield driver
#
#     logger.info("========== CLOSING TEST ==========")
#
#     try:
#
#         driver.quit()
#
#         logger.info("BROWSER CLOSED SUCCESSFULLY")
#
#     except Exception as e:
#
#         logger.error(
#             f"ERROR CLOSING BROWSER: {str(e)}"
#         )
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#
#     report = outcome.get_result()
#
#     if report.when == "call":
#
#         if "driver" not in item.funcargs:
#             return
#
#         driver = item.funcargs["driver"]
#
#         try:
#
#             if report.passed:
#
#                 logger.info(
#                     "TEST PASSED - CAPTURING SCREENSHOT"
#                 )
#
#                 path = ScreenshotUtil.capture(
#                     driver,
#                     f"{item.name}_PASS"
#                 )
#
#             else:
#
#                 logger.error(
#                     "TEST FAILED - CAPTURING SCREENSHOT"
#                 )
#
#                 path = ScreenshotUtil.capture(
#                     driver,
#                     f"{item.name}_FAIL"
#                 )
#
#             allure.attach.file(
#                 path,
#                 name="Screenshot",
#                 attachment_type=allure.attachment_type.PNG
#             )
#
#         except Exception as e:
#
#             logger.error(
#                 f"SCREENSHOT FAILED: {str(e)}"
#             )
#
# import subprocess
# import os
#
# def pytest_unconfigure(config):
#
#     project_path = r"C:\Users\DELL\OneDrive\Desktop\wipro capstone\Makemytrip"
#
#     allure_results = os.path.join(project_path, "allure-results")
#     allure_report = os.path.join(project_path, "allure-report")
#
#     allure_path = os.path.expandvars(
#         r"%USERPROFILE%\scoop\apps\allure\current\bin\allure.bat"
#     )
#
#     try:
#
#         # Generate report permanently inside project
#         subprocess.run(
#             f'"{allure_path}" generate "{allure_results}" -o "{allure_report}" --clean',
#             shell=True,
#             check=True
#         )
#
#         # Open report automatically
#         subprocess.Popen(
#             f'"{allure_path}" open "{allure_report}"',
#             shell=True
#         )
#
#         print("ALLURE REPORT GENERATED SUCCESSFULLY!")
#
#     except Exception as e:
#         print(f"ALLURE ERROR : {e}")
import pytest
import allure
import time
import os
import subprocess

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
    driver.get("https://www.makemytrip.com/hotels/")

    # CRITICAL WAF WAIT: Let invisible security scripts resolve
    time.sleep(2)

    logger.info(f"CURRENT URL: {driver.current_url}")

    yield driver

    logger.info("========== CLOSING TEST ==========")
    try:
        driver.quit()
        logger.info("BROWSER CLOSED SUCCESSFULLY")
    except Exception as e:
        logger.error(f"ERROR CLOSING BROWSER: {str(e)}")


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
                logger.info("TEST PASSED - CAPTURING SCREENSHOT")
                path = ScreenshotUtil.capture(driver, f"{item.name}_PASS")
            else:
                logger.error("TEST FAILED - CAPTURING SCREENSHOT")
                path = ScreenshotUtil.capture(driver, f"{item.name}_FAIL")

            allure.attach.file(
                path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logger.error(f"SCREENSHOT FAILED: {str(e)}")



# AUTO GENERATE AND OPEN ALLURE REPORT
def pytest_unconfigure(config):
    print("\n======= TESTS COMPLETED - GENERATING ALLURE REPORT =======")

    # Ensure the results directory exists to avoid generation errors
    if not os.path.exists("reports/allure-results"):
        os.makedirs("reports/allure-results")

    # Compile JSON results into static HTML in the reports/allure-report directory
    os.system("allure generate reports/allure-results -o reports/allure-report --clean")

    # Open the generated HTML report

    os.system("allure open reports/allure-report")