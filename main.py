import tushare as ts
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns

min_data_dir = '/home/prod/data/stock_min_data'
cal_dates = ts.trade_cal()

def get_min_line(symbol, begin_date, end_date=None):
	df=pd.DataFrame()	
	str_begin_date = str(begin_date)
	if (end_date == None):
		if is_open_day(str_begin_date):
			min_dir = min_data_dir + '/' + symbol + '/' + str(begin_date.year) + '/' + str(begin_date.month)
			min_data_file=min_dir + '/' + symbol + '_' + str_begin_date + '_1min_data.h5'
			if(os.path.exists(min_data_file)):
				hdf5_file = pd.HDFStore(min_data_file, 'r')
				df = hdf5_file['data']
				hdf5_file.close()
				print("Successfully read min_data_file file: " + min_data_file)
				return df
	else:
		dates=get_date_list(begin_date,end_date)
		for date in dates:
			str_date = str(date)
			if is_open_day(str_date):
				min_dir = min_data_dir + '/' + symbol + '/' + str(date.year) + '/' + str(date.month)
				min_data_file=min_dir + '/' + symbol + '_' + str_date + '_1min_data.h5'
				if(os.path.exists(min_data_file)):
					hdf5_file = pd.HDFStore(min_data_file, 'r')
					df=df.append(hdf5_file['data'])
					hdf5_file.close()
					print("Successfully read min_data_file file: " + min_data_file)
		print(symbol)
		print(df)
		return df

def get_date_list(begin_date, end_date):
	date_list = []
	while begin_date <= end_date:
		date_list.append(begin_date)
		begin_date += datetime.timedelta(days=1)
	return date_list

def get_all_stock_id():
    stock_info = ts.get_hs300s()
    return stock_info['code'].values

def is_open_day(date):
    if date in cal_dates['calendarDate'].values:
        return cal_dates[cal_dates['calendarDate'] == date].iat[0, 1] == 1
    return False

def plot_corr_matrix(begin_date,end_date=None):
	stocks = get_all_stock_id()
	corr_source_data=pd.DataFrame()
	for stock in stocks:
		stockdf=get_min_line(stock,begin_date,end_date)
		print(stockdf)
		columns = ['high', 'open', 'close', 'volume', 'amount']
		stockdf.drop(columns, inplace=True, axis=1)
		stockdf.rename(columns={'low': stock}, inplace=True)
		corr_source_data=pd.concat([corr_source_data, stockdf], axis=1)
#	stockdf=get_min_line('600482',begin_date,end_date)
#	columns = ['open', 'high', 'close', 'volume', 'amount']
#	print(stockdf)
#	stockdf.drop(columns, inplace=True, axis=1)
#	stockdf.rename(columns={'low': '600482'}, inplace=True)
#	corr_source_data=pd.concat([corr_source_data, stockdf], axis=1)
	plt.matshow(dataframe.corr())
	
if __name__ == '__main__':
	plot_corr_matrix(datetime.date(2017, 10, 30), datetime.date.today())
