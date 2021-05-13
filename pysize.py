import csv
from datetime import datetime
import shutil
import os
import json

# Version 0.3

class PySize():
    def __init__(self):
        self.json_data = {}
        self.json_data_path = os.path.join(os.path.dirname(__file__), "pysize-data.json")
        self.date_format = "%Y-%m-%d-%H:%M:%S"
        self.output_date_format = "%d/%m/%Y %H:%M:%S"

    def load(self):
        with open(self.json_data_path, "r") as json_data:
            self.json_data = json.load(json_data)

    def save(self):
        with open(self.json_data_path, "w") as json_data:
            json.dump(self.json_data, json_data, indent=4, sort_keys=True)

    def add_record(self):
        """ In Bytes"""

        date = datetime.now().strftime(self.date_format)
        total, used, free = shutil.disk_usage(self.json_data["config"]["root"])
        #unit = self.json_data["config"]["unit"]

        record = {"unit": "bytes",
                  "date": date,
                  "bytes_total": total,
                  "bytes_used": used,
                  "bytes_free": free
                  }

        self.json_data["data"].append(record)
        return record


    def export_to_csv(self, filename="export.csv"):
        if not self.json_data:
            Exception("Please load the data file before !")

        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fields = ["Date", "Total", "Used", "Free", "Unit"]
            writer = csv.DictWriter(csv_file, fieldnames=fields)

            writer.writeheader()
            for record in self.json_data["data"]:

                date_object = datetime.strptime(record["date"], self.date_format)
                date = date_object.strftime(self.output_date_format)

                row_data = [date,
                            record["bytes_total"],
                            record["bytes_used"],
                            record["bytes_free"],
                            record["unit"]]

                csv_writer.writerow(row_data)

            msg = "{} row(s) exported.".format(len(self.json_data["data"]))
            print(msg)


    def export_to_chart(self, filename="chart.png"):
        if not self.json_data:
            Exception("Please load the data file before !")

        filepath = os.path.join(os.path.dirname(__file__), filename)

        from matplotlib import pyplot

        x_date = [] # Date
        y_used = [] # Used
        y_total = [] # Total

        for index, record in enumerate(self.json_data["data"]):

            date_object = datetime.strptime(record["date"], self.date_format)
            date = date_object.strftime(self.output_date_format)

            used = (record["bytes_used"] / 8) / (1024 ^ 3)
            total = (record["bytes_total"] / 8) / (1024 ^ 3)

            x_date.append(date)
            y_used.append(used)
            y_total.append(total)

        # Draw lines
        pyplot.plot(x_date, y_total, linestyle="-", marker="o", color="b")
        pyplot.plot(x_date, y_used, linestyle="-", marker="o", color="r")

        # Force 0 to show in graph
        pyplot.ylim(ymin=0)
        pyplot.xticks(rotation=90)
        pyplot.tight_layout() # Avoid xticks to be outside of the image
        pyplot.savefig(filepath)

if __name__ == "__main__":
    pysize = PySize()
    pysize.load()
    pysize.add_record()
    pysize.save()
    pysize.export_to_csv()
    #pysize.export_to_chart()
