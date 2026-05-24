import csv

class CsvReader:
    @staticmethod
    def get_data_by_scenario(file_path, scenario_name):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Matches the 'test_scenario' column in your CSV
                if row['test_scenario'] == scenario_name:
                    return row
        raise ValueError(f"Scenario '{scenario_name}' not found in {file_path}")

    @staticmethod
    def get_test_data(file_path, row_index):
        # Your existing logic for positive scenarios (by index)
        with open(file_path, mode='r', encoding='utf-8') as file:
            rows = list(csv.DictReader(file))
            return rows[int(row_index) - 1]