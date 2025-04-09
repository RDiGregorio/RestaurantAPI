import re
from dateutil.parser import parse

# Extracts a time range (e.g., "9:00 am - 5:00 pm") from a given string.
# Returns the matched time range or None if no match is found.
def time_range(string):
    pattern = r'\d+(:\d{2})? (am|pm) - \d+(:\d{2})? (am|pm)'
    match = re.search(pattern, string)
    return match.group(0) if match else None

# Converts a time range string (e.g., "9:00 am - 5:00 pm") into a list of datetime objects.
# Returns a list of two datetime objects representing the start and end times.
def time_range_to_dates(string):
    return list(map(parse, string.split("-")))

# Extracts date ranges (e.g., "Mon-Wed") or individual days (e.g., "Fri") from a given string.
# Returns a list of matched date ranges or days.
def date_ranges(string):
    pattern = r'\w{3}(?:-\w{3})?'
    result = []
    matches = re.finditer(pattern, string)

    for match in matches:
        result.append(match.group())

    return result

# Expands a date range (e.g., "Mon-Wed") into a list of individual days (e.g., ["Mon", "Tue", "Wed"]).
# If a single day is provided, returns it as a list.
def expand_date_range(range):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start, *end = range.split("-")
    if end:
        return days[days.index(start):days.index(end[0]) + 1]
    return [start]

# Extracts and parses the start date from a time range string (e.g., "9:00 am - 5:00 pm").
def start_date(string):
    return parse(string.split("-")[0])

# Extracts and parses the end date from a time range string (e.g., "9:00 am - 5:00 pm").
def end_date(string):
    return parse(string.split("-")[1])