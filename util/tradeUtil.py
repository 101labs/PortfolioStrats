#!/usr/bin/python
import tushare as ts
import datetime

cal_dates = ts.trade_cal()
commision_percent = 0.3 
Lowbarrier = 5



def is_open_day(date, region='cn'):
	# Check if it is trading day for specified region
    if region == 'cn':
    	if date in cal_dates['calendarDate'].values:
        	return cal_dates[cal_dates['calendarDate'] == date].iat[0, 1] == 1
    	return False
    else return 0


def get_date_list(begin_date, end_date):
    date_list = []
    while begin_date <= end_date:
        date_list.append(begin_date)
        begin_date += datetime.timedelta(days=1)
    return date_list


def get_business_date_list(begin_date, end_date, region='cn'):
	# Return a list with open days
	date_list = []
    while ((begin_date <= end_date) && is_open_day(begin_date,region)):
        date_list.append(begin_date)
        begin_date += datetime.timedelta(days=1)
    return date_list

def get_hs300s_id():
    stock_info = ts.get_hs300s()
    return stock_info['code'].values

def get_all_stock_id():
    #To Do
    #最好可以获取全部股票id
    stock_info = ts.get_hs300s()
    stock_info=ts.get_stock_basics()
    codes = list(stock_info.index.values)
    return codes

def cal_fee_cost(price, amount):
   #当前手续费0.3%，最低5元起
   #希望以后有个setting文件，参数不写死
   #To do
   global Lowbarrier, commision_percent
   commission = price*amount*commision_percent
    if commission > Lowbarrier:
            return commission
        else:
            return Lowbarrier

def get_stock_operation_value(code, date, direction,amount):
	#对股票实行买入卖出操作
	#code = stockid
	#date = operation date
	#direction = 'short' or 'long' long是买入 short是卖出
	#amount = 股票买卖数量
	#return = 收益或者支出,收益时为正，支出时为负,需考虑手续费
	#To do

	#df = self.data_repository.get_onecode_df(code)
        df = ts.get_hist_data(code)
	buy_signal = 0
	buy_open_price = 0
        if date not in list(df.index.values):
	#if df[df['date'] == date].empty:
	    return buy_signal, buy_open_price

        #df = df[df['date'] <= date].tail(3)
	#if len(df) == 3 and df.iloc[0]['ma5'] < df.iloc[0]['ma10'] and df.iloc[1]['ma5'] > df.iloc[1]['ma10']:
	#buy_signal = 1
	#buy_open_price = df.iloc[1]['open']
        closeprice = df.loc[date].close
        buy_open_price = amount*closeprice
        fee = buy_open_price*commision_percent*0.01
        if fee<Lowbarrier:
            fee = Lowbarrier
        if direction == 'short':
            buy_signal = 1
        elif direction == 'long':
            buy_signal = -1
	return buy_signal*buy_open_price-fee

