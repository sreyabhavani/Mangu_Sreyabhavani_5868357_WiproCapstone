import csv
import os
from utils.logger import AutomationLogger

# FIXED: Now calls the unified AutomationLogger class and get_logger method
logger = AutomationLogger.get_logger("CSVReader")


class CSVReader:

    @staticmethod
    def read_csv(file_name):
        data = []
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            file_name
        )

        logger.info(f"POM LOG: Attempting to read CSV from path: {path}")

        try:
            # Added encoding='utf-8' for safety
            with open(path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)

            logger.info(f"POM LOG: Successfully read {len(data)} rows from {file_name}")
            return data

        except FileNotFoundError:
            logger.error(f"POM LOG: CSV file not found at: {path}")
            raise
        except Exception as e:
            logger.error(f"POM LOG: Error reading CSV {file_name}: {str(e)}")
            raise