import csv


class CSVReader:

    @staticmethod
    def read_data(file_path):

        data_list = []

        with open(file_path, newline='') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                data_list.append(row)

        return data_list