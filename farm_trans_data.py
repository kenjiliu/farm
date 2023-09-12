# -*- coding: utf-8 -*-
# 
# 農產品市場交易價格查詢
#
import sys
import requests
import json
import time
from datetime import datetime, date, timedelta

def minguo_to_xiyuan(convert_date, sep='.'):
	"""民國轉西元， Convert '109.07.01' to '2020.07.01' """
	y, m, d = str(convert_date).split(sep)
	return str(int(y)+1911) + sep + m  + sep + d

def xiyuan_to_minguo(convert_date, sep='.'):
	"""西元轉民國， Convert '2020.07.01' to '109.07.01' """
	y, m, d = str(convert_date).split(sep)
	return str(int(y)-1911) + sep + m  + sep + d

def days_ago(n):
	""" return n days ago date and convert date format to 'YYY.mm.dd' """
	now_date = datetime.today().date()
	day_ago = now_date - timedelta(days = n)
	fm_minguo_dot = xiyuan_to_minguo(day_ago, '-').replace('-', '.')
	return fm_minguo_dot

today = days_ago(0)
ndays_ago = days_ago(1) # set N days ago
now_time = time.strftime("%H:%M:%S")
day_time = time.strftime("%Y-%m-%d %H:%M:%S")
columns = ['交易日期', '種類代碼', '作物代號', '作物名稱', '市場代號', '市場名稱', '上價', '中價', '下價', '平均價', '交易量']

def get_trans_data(crop_code, market, start_date=today, end_date=today, raw_data=False):
	"""
	【農產品市場交易價格查詢】
	資料來源：
	行政院農業委員會資料開放平台
	https://data.coa.gov.tw/Query/AdvSearch.aspx?id=037
	資料查詢網址：(json)
	https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx?$top=1000&$skip=0

	參數說明：
	crop_code, 作物代碼
	market, 市場名稱
	start_date, 開始日期，預設當日日期 （日期格式：YYY.mm.dd 其中YYY為民國年）
	end_date, 結束日期，預設當日日期 （日期格式：YYY.mm.dd 其中YYY為民國年）
	raw_data, raw data is dict contents with keys and values, default ie False, it's list contents
	"""
	try:
		api_url = 'https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx'
		payload = {'CropCode': crop_code, 'Market': market, 'StartDate': start_date, 'EndDate': end_date} 
		response = requests.get(api_url, params=payload)
		# print(response.url)
		# print(response.status_code)
		#if response.status_code == requests.codes.ok: #測試連線狀況
		result = json.loads(response.text)

		dataframe = list()	
		if result:
			for dict_item in result: # use reversed(result) to sort reverse
				cols = list()
				for col_item in columns:
					for keys, values in dict_item.items():
						if col_item == keys:
							cols.append(values)
				dataframe.append(cols)
		
		if raw_data:
			return result
		else:
			return dataframe
	except:
		print('連線錯誤！請檢查網路狀況～')
		sys.exit()

def get_trans_data_list(crop, market, start_date, end_date):
	list_items = get_trans_data(crop, market, start_date, end_date, True)
	dataframe = []
	
	for dict_items in list_items:
		cols = []
		for col_item in columns:
			for key, values in dict_items.items():
				if col_item == key:
					cols.append(values)
		dataframe.append(cols)
	return dataframe

def check_market_rest(market, check_date=today):
	"""
	用於檢查交易市場是否休市：
	market 市場名稱
	check_date 要檢查的日期 （日期格式：YYY.mm.dd 其中YYY為民國年）
	"""
	crop_code = 'rest'
	result = get_trans_data(crop_code, market, check_date, check_date)
	if result:
		return True #休市
	else:
		return False

def price_list(crop_code, markets):
	""" 
	return the short information
	以較短的格式回傳今日的各市場價格，只回傳市場名稱欄位以後的資訊
	"""
	items = ''
	items_list = list()
	for market in markets:
		if check_market_rest(market, today):
			items = '{}	[本日休市]'.format(market)
			items_list.append(items)
		else:
			data = get_trans_data(crop_code, market, today)
			if data:
				for item in data:
					items = ''
					i = item.index(market) # 從市場名稱開始取得資料
					for cols in range(i, len(item)):
						if i == (len(item) - 1):
							items += str(item[cols]) + ' '
						else:
							items += str(item[cols]) + ' | '
							i += 1
					#print(items)
					items_list.append(items)
			else:
				items_list = []
				#items_list.append('{}	[查無資料] @{}'.format(market, now_time))	

	return items_list

def price_list_html(crop_code, markets):
	""" 
	return the short information
	以較短的格式回傳今日的各市場價格，只回傳市場名稱欄位以後的資訊
	"""
	items = ''
	items_list = list()
	for market in markets:
		if check_market_rest(market, today):
			items = '<tr style="background-color: white;"><td style="padding: 10px;">{}</td><td colspan="5">[本日休市]</td></tr>'.format(market)
			items_list.append(items)
		else:
			data = get_trans_data(crop_code, market, today)
			if data:
				for item in data:
					items = '<tr style="background-color: white;"><td style="padding: 10px; text-align: right;">'
					i = item.index(market) # 從市場名稱開始取得資料
					for cols in range(i, len(item)):
						if i == (len(item) - 1):
							items += str(item[cols]) + '</td></tr>'
						else:
							items += str(item[cols]) + '</td><td style="padding: 10px; text-align: right;">'
							i += 1
					#print(items)
					items_list.append(items)

	return items_list

def price_list_bootstrap(crop_code, markets):
	""" 
	return the short information
	以較短的格式回傳今日的各市場價格，只回傳市場名稱欄位以後的資訊
	"""
	items = ''
	items_list = list()
	for market in markets:
		if check_market_rest(market, today):
			items = '<tr><td>{}</td><td colspan="5">[本日休市]</td></tr>'.format(market)
			items_list.append(items)
		else:
			data = get_trans_data(crop_code, market, today)
			if data:
				for item in data:
					items = '<tr><td>'
					i = item.index(market) # 從市場名稱開始取得資料
					for cols in range(i, len(item)):
						if i == (len(item) - 1):
							items += str(item[cols]) + '</td></tr>'
						else:
							items += str(item[cols]) + '</td><td>'
							i += 1
					#print(items)
					items_list.append(items)
				#print(items_list)
	return items_list

def main():
	sep_num = 92

	def print_title():
		print('-' * sep_num)
		for i in columns:
			print(i, end='  ')
		print()
		print('-' * sep_num)

	# 想要的品種
	crop_codes = ['G3','G2']
	# 想要的市場
	markets = ['台北一','台北二']
	# 設定 start_date 和 end_date 範圍 （ex. 103.01.01）
	start_date = ndays_ago
	end_date = today

	# when retun raw result
	# for crop in crop_codes:
	# 	for market in markets:
	# 		list_items = get_trans_data(crop, market, start_date, end_date, True)
	# 		for dict_items in list_items:
	# 			for col_item in columns:
	# 				for key, values in dict_items.items():
	# 					if col_item == key:
	# 						print(values, end='  ')
	# 			print()


	# when return dataframe
	if get_trans_data(crop_codes[0], markets[0],start_date,end_date):
		print_title()
		for crop_code in crop_codes:
			for market in markets:
				list_items = get_trans_data(crop_code, market, start_date, end_date)
				for items in list_items:
					for rows in items:
						print(rows, end='	')
					print()
				#print('-' * sep_num)
	else:
		print('查無資料！')

if __name__ == '__main__':
	main()
