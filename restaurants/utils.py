import re
from dateutil.parser import parse

def time_range(string):
    pattern = r'\d+(:\d{2})? (am|pm) - \d+(:\d{2})? (am|pm)'
    match = re.search(pattern, string)
    return match.group(0) if match else None

def time_range_to_dates(string):
    return list(map(parse, string.split("-")))

def date_ranges(string):
    pattern = r'\w{3}(?:-\w{3})?'
    result = []
    matches = re.finditer(pattern, string)

    for match in matches:
        result.append(match.group())

    return result

def expand_date_range(range):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start, *end = range.split("-")
    if end:
        return days[days.index(start):days.index(end[0]) + 1]
    return [start]



