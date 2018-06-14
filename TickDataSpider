# coding=utf-8
import tushare as ts
import pandas as pd
import numpy as np
import math
import datetime
import time
import os


data_dir = '/home/tianjiawei/PortfolioStrats/data/stock_tick_data'
sleep_time = 0.2
cal_dates = ts.trade_cal()


def is_open_day(date):
    if date in cal_dates['calendarDate'].values:
        return cal_dates[cal_dates['calendarDate'] == date].iat[0, 1] == 1
    return False


def get_save_tick_data(symbol, date):
    global sleep_time, data_dir
    res = True
    str_date = str(date)
    dir = data_dir + '/' + symbol + '/' + \
        str(date.year) + '/' + str(date.month)
    file = dir + '/' + symbol + '_' + str_date + '_tick_data.h5'
    if is_open_day(str_date):
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(file):
            try:
                d = ts.get_tick_data(symbol, str_date, pause=0.1)
            except IOError as msg:
                print(msg)
                # 每次下载失败后sleep_time翻倍，但是最大128s
                sleep_time = min(sleep_time * 2, 128)
                print('Get tick data error: symbol: ' + symbol + ', date: ' +
                      str_date + ', sleep time is: ' + str(sleep_time))
                return res
            else:
                hdf5_file = pd.HDFStore(
                    file, 'w', complevel=4, complib='blosc')
                hdf5_file['data'] = d
                hdf5_file.close()
                # 每次成功下载后sleep_time变为一半，但是至少2s
                sleep_time = max(sleep_time / 2, 2)
                print("Successfully download and save file: " +
                      file + ', sleep time is: ' + str(sleep_time))
                return res
        else:
            print("Data already downloaded before, skip " + file)
            res = False
            return res


def get_date_list(begin_date, end_date):
    date_list = []
    while begin_date <= end_date:
        #date_str = str(begin_date)
        date_list.append(begin_date)
        begin_date += datetime.timedelta(days=1)
    return date_list


def get_all_stock_id():
    stock_info = ts.get_hs300s()
    return stock_info['code'].values

dates = get_date_list(datetime.date(2017, 10, 30), datetime.date(2018, 6, 14))
stocks = get_all_stock_id()
for stock in stocks:
    for date in dates:
        if get_save_tick_data(stock, date):
            time.sleep(sleep_time)
