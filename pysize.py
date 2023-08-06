# Version 0.4

import argparse
import os
import shutil
import csv
import json

from datetime import datetime


class PySize:
    def __init__(self):
        self.json_data = {}
        self.json_data_path = os.path.join(os.path.dirname(__file__), "pysize-data.json")
        self.date_format = "%Y-%m-%d %H:%M:%S" # TODO: Déplacer dans le fichier de config
        self.output_date_format = "%d/%m/%Y %H:%M:%S" # TODO: Déplacer dans le fichier de config

    def load(self):
        with open(self.json_data_path, "r") as json_data:
            self.json_data = json.load(json_data)

        msg = "{} records(s) loaded from file.".format(len(self.json_data["data"]))
        print(msg)

    def save(self):
        with open(self.json_data_path, "w") as json_data:
            json.dump(self.json_data, json_data, indent=4, sort_keys=True)

        msg = "{} records(s) saved to file.".format(len(self.json_data["data"]))
        print(msg)

    def create_record(self):
        """ In Bytes"""

        date = datetime.now().strftime(self.date_format)
        total, used, free = shutil.disk_usage(self.json_data["config"]["root"])

        record = {
            "date": date,
            "total": total,
            "used": used
        }

        msg = "A new record was created."
        print(msg)

        self.json_data["data"].append(record)
        return record

    def export_to_csv(self, filename="pysize-export.csv"):
        if not self.json_data:
            Exception("Please load the data file before !")

        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fields = ["Date", "Used", "Total", "Comment"]
            writer = csv.DictWriter(csv_file, fieldnames=fields)

            writer.writeheader()
            for record in self.json_data["data"]:
                date_object = datetime.strptime(record["date"], self.date_format)
                date = date_object.strftime(self.output_date_format)

                row_data = [date,
                            record["used"],
                            record["total"],
                            record["comment"] if "comment" in record else ""]

                csv_writer.writerow(row_data)

            msg = "{} row(s) exported.".format(len(self.json_data["data"]))
            print(msg)

    def export_to_chart(self, filename="pysize-export.png"):
        if not self.json_data:
            Exception("Please load the data file before !")

        filepath = os.path.join(os.path.dirname(__file__), filename)

        x_date = []  # Date
        y_used = []  # Used
        y_total = []  # Total

        for index, record in enumerate(self.json_data["data"]):
            date_object = datetime.strptime(record["date"], self.date_format)
            date = date_object.strftime(self.output_date_format)

            used = (record["used"] / 8) / (1024 ^ 3)
            total = (record["total"] / 8) / (1024 ^ 3)

            x_date.append(date)
            y_used.append(used)
            y_total.append(total)

        # Draw lines
        linestyle = self.json_data["config"]["graph"]["total"]["linestyle"]
        marker = self.json_data["config"]["graph"]["total"]["marker"]
        color = self.json_data["config"]["graph"]["total"]["color"]
        pyplot.plot(x_date, y_total, linestyle=linestyle, marker=marker, color=color)

        linestyle = self.json_data["config"]["graph"]["used"]["linestyle"]
        marker = self.json_data["config"]["graph"]["used"]["marker"]
        color = self.json_data["config"]["graph"]["used"]["color"]
        pyplot.plot(x_date, y_used, linestyle=linestyle, marker=marker, color=color)

        # Force 0 to show in graph
        pyplot.ylim(ymin=0)
        pyplot.xticks(rotation=90)
        pyplot.tight_layout()  # Avoid xticks to be outside of the image
        pyplot.savefig(filepath)

        msg = "Chart output was saved to {}".format(filepath)
        print(msg)

    def create_daily_record(self):
        record_of_the_day_exists = self._filter_daily_records()

        if record_of_the_day_exists:
            print("A record already exists for the day. Skipping.")
        else:
            self.create_record()
            self.save()

    def _filter_daily_records(self):
        now = datetime.now()

        already_exists = False

        # On inverse car le dernier jour est forcément dans les derniers
        for record in reversed(self.json_data["data"]):
            record_datetime = datetime.strptime(record["date"], self.date_format)
            if record_datetime.date() == now.date():
                already_exists = True
                break

        return already_exists


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--csv", default=False, action='store_true')
    argument_parser.add_argument("--chart", default=False, action='store_true')
    argument_parser.add_argument("--create-record", default=False, action='store_true')
    argument_parser.add_argument("--create-daily-record", default=False, action='store_true')

    args = argument_parser.parse_args()

    pysize = PySize()
    pysize.load()

    if args.create_daily_record:
        pysize.create_daily_record()
        pysize._filter_daily_records()

    if args.create_record:
        pysize.create_record()
        pysize.save()

    if args.csv:
        pysize.export_to_csv()

    if args.chart:
        from matplotlib import pyplot

        pysize.export_to_chart()
