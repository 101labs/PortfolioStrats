#!/usr/bin/python
import tushare as ts
import datetime

cal_dates = ts.trade_cal()
def is_open_day(date):
    if date in cal_dates['calendarDate'].values:
        return cal_dates[cal_dates['calendarDate'] == date].iat[0, 1] == 1
    return False


def get_date_list(begin_date, end_date):
    date_list = []
    while begin_date <= end_date:
        date_list.append(begin_date)
        begin_date += datetime.timedelta(days=1)
    return date_list
