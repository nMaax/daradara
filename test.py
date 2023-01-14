from datetime import datetime
from dateutil import parser as date_parser

py_date = date_parser.parse("2023-01-14")

print(py_date)

# Get the current date and time
now = datetime.today()

# Set the hour to a specific value (e.g. 14)
#new_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
new_time = now

print(new_time)

print(py_date == new_time)
