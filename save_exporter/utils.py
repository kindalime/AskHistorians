import datetime

def get_unix_time(year, month, day, timezone):
    date = datetime.datetime(year, month, day)
    date = timezone.localize(date)
    stamp = date.timestamp()
    return stamp