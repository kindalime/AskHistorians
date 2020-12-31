import datetime
import pytz
from tzlocal import get_localzone

def get_unix_time(date):
    date = datetime.datetime.combine(date, datetime.time())
    date = get_localzone().localize(date)
    stamp = date.timestamp()
    return stamp
