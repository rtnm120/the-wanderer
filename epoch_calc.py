#!/usr/bin/env python3
import datetime
import calendar


def get_epoch():
    utc_now = datetime.datetime.utcnow()
    year = utc_now.year
    month = utc_now.month
    day = utc_now.day
    hour = utc_now.hour

    months = [1, 3, 5, 7, 8, 10, 12]

    if hour >= 5 and hour < 10:
        expiry = datetime.datetime(year, month, day, 10, 30, 0)
    elif hour >= 11 and hour < 17:
        expiry = datetime.datetime(year, month, day, 16, 30, 0)
    elif hour >= 17 and hour < 23:
        expiry = datetime.datetime(year, month, day, 22, 30, 0)
    elif hour < 5:
        expiry = datetime.datetime(year, month, day, 4, 30, 0)
    else:
        if month in months and day == 31:
            if month == 12:
                expiry = datetime.datetime(year + 1, 1, 1, 4, 30, 0)
            else:
                expiry = datetime.datetime(year, month + 1, 1, 4, 30, 0)
        elif month == 2:
            if day == 28 and calendar.isleap(year):
                expiry = datetime.datetime(year, month, 29, 4, 30, 0)
            elif day == 29:
                expiry = datetime.datetime(year, 3, 1, 4, 30, 0)
            else:
                expiry = datetime.datetime(year, month, day + 1, 4, 30, 0)
        else:
            if day == 30:
                expiry = datetime.datetime(year, month + 1, 1, 4, 30, 0)
            else:
                expiry = datetime.datetime(year, month, day, 4, 30, 0)

    epoch_expiry = calendar.timegm(expiry.timetuple())
    return epoch_expiry


if __name__ == "__main__":
    print(get_epoch())
