

import pytest
import allure
import time
import os

# IMPORT SELENIUMBASE
from seleniumbase import Driver

from utils.logger import LogGen
#from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


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
        "https://www.makemytrip.com/bus-tickets/"
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
#import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()