from dateutil.parser import parse

def time_range_to_dates(string):
    return list(map(parse, string.split("-")))