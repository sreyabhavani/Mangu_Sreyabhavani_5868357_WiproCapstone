import logging
import os


class AutomationLogger:

    @staticmethod
    def get_logger(name="Automation"):

        if not os.path.exists("logs"):
            os.makedirs("logs")

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Clear existing handlers to prevent duplicate log lines
        if logger.hasHandlers():
            logger.handlers.clear()

        file_handler = logging.FileHandler("logs/automation.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger