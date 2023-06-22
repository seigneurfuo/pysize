import json
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d-%H:%M:%S"
NEW_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

input_file =  open("pysize-data.json", "r")
output_file = open("pysize-data-v2.json", "w")

data = json.load(input_file)

# Output file

for index, record in enumerate(data["data"]):
    # Convert date to new format
    date = datetime.strptime(record["date"], DATE_FORMAT)
    record["date"] = date.strftime(NEW_DATE_FORMAT)

    # Renaming keys
    record["used"] = record["bytes_used"]
    record["total"] = record["bytes_total"]

    # Removing unused keys
    del record["bytes_free"]
    del record["unit"]

    # Revoving old keys
    del record["bytes_used"]
    del record["bytes_total"]

json.dump(data, output_file, indent=4, sort_keys=True)