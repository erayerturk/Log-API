import pytz
from dateutil.parser import parse


def convert_date(date_str):
    return parse(date_str).replace(tzinfo=pytz.timezone("Europe/Istanbul"))
