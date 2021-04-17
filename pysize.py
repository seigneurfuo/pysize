import csv
from datetime import datetime
import shutil
import os
import json

class PySize():
    def __init__(self):
        self.json_data = {}
        self.json_data_path = os.path.join(os.path.dirname(__file__), "pysize-data.json")

    def load(self):
        with open(self.json_data_path, "r") as json_data:
            self.json_data = json.load(json_data)

    def save(self):
        with open(self.json_data_path, "w") as json_data:
            json.dump(self.json_data, json_data, indent=4, sort_keys=True)

    def add_record(self):
        """ In Bytes"""

        date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        total, used, free = shutil.disk_usage(self.json_data["config"]["root"])
        #unit = self.json_data["config"]["unit"]

        # Bits par GigaByte
        bytes_per_GB = 1024 * 1024 * 1024

        total /= bytes_per_GB
        used /= bytes_per_GB
        free /= bytes_per_GB


        record = {"unit": self.json_data["config"]["unit"],
                  "date": date,
                  "total": total,
                  "used": used,
                  "free": free
                  }

        self.json_data["data"].append(record)
        return record


    def export_to_csv(self):
        if not self.json_data:
            Exception("Please load the data file before !")

        with open("export.csv", 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fields = ["Total", "Used", "Free", "Unit"]
            writer = csv.DictWriter(csv_file, fieldnames=fields)

            writer.writeheader()
            for record in self.json_data["data"]:
                row_data = [record["date"],
                            record["total"],
                            record["used"],
                            record["free"],
                            record["unit"]]

                csv_writer.writerow(row_data)

            msg = "{} row(s) exported.".format(len(self.json_data["data"]))
            print(msg)

if __name__ == "__main__":
    pysize = PySize()
    pysize.load()
    pysize.add_record()
    pysize.save()
    #pysize.export_to_csv()