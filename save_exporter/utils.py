import datetime
import pytz
from tzlocal import get_localzone

def get_unix_time(date):
    date = datetime.datetime.combine(date, datetime.time())
    date = get_localzone().localize(date)
    stamp = date.timestamp()
    return stamp

def get_date(timestamp):
    date = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    date = date.astimezone(get_localzone())
    return date

if __name__ == "__main__":
    date = datetime.date(2021, 1, 1)
    print(date)
    stamp = get_unix_time(date)
    print(stamp)
    new = get_date(stamp)
    print(new)
