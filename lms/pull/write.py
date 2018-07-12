import json
import csv


def json_file(directory, name, json_data):
    """creates a name.json file of the data at the given directory"""

    with open(directory + name + '.json', 'w') as f:
        json.dump(json_data, f)


def csv_file(directory, name, csv_data):
    """creates a name.csv file of the data at the given directory"""

    with open(directory + name + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        reader = csv.reader(csv_data.text.splitlines())
        for row in reader:
            writer.writerow(row)
