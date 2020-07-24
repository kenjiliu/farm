# -*- coding: utf-8 -*-
# farm-trans-data.py

import requests
import json
import time
from datetime import datetime, date, timedelta

def minguo_to_xiyuan(convert_date, sep='/'):   #民國轉西元
	y, m, d = str(convert_date).split(sep)
	return str(int(y)+1911) + sep + m  + sep + d

def xiyuan_to_minguo(convert_date, sep='/'):   #西元轉民國
	y, m, d = str(convert_date).split(sep)
	return str(int(y)-1911) + sep + m  + sep + d

def days_ago(n):
	now_date = datetime.today().date()
	day_ago = now_date - timedelta(days = n)
	#day_ago = now_date.replace(day=now_date.day - n)
	fm_minguo_dot = xiyuan_to_minguo(day_ago, '-').replace('-', '.')
	return fm_minguo_dot

today = days_ago(0)
ndays_ago = days_ago(5)

def get_trans_data(crop_code, market, start_date, end_date=today):
	api_url = 'https://data.coa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx'
	payload = {'CropCode': crop_code, 'Market': market, 'StartDate': start_date, 'EndDate': end_date} 
	response = requests.get(api_url, params=payload)
	# print(response.url)
	# print(response.status_code)
	if response.status_code == requests.codes.ok: #測試連線狀況
		result = json.loads(response.text)
	
	dataframe = list()	
	if result:
		for dict_list in result: # use reversed(result) to sort reverse
			cols = list()
			for item in dict_list.values():
				cols.append(item) # equal to dict_list[item] without values()
			dataframe.append(cols)
	return dataframe
	#return result #raw result

def get_trans_data_all(crop_codes, markets, start_date, end_date=today):
	dataframe = list()	
	for crop_code in crop_codes:
		for market in markets:
			gtd = get_trans_data(crop_code, market, start_date, end_date)
			if gtd:
				for cols in gtd:
					dataframe.append(cols)
	return dataframe


if __name__ == '__main__':

	def title():
		columns = ['交易日期', '作物代號', '作物名稱', '市場代號', '市場名稱', '上價', '中價', '下價', '平均價', '交易量']
		print('-' * 87)
		for i in columns:
			print(i, end='  ')
		print()
		print('-' * 87)

# 想要的品種
	crop_codes = ['G3','G2']
# 想要的市場
	markets = ['台北一', '台北二']
# 設定 start_date 和 end_date 範圍 （ex. 103.01.01）
	start_date = ndays_ago
	end_date = today

# when retun raw result
# for crop in crops:
# 	for market in markets:
# 		dataframe = get_trans_data(crop, market, start_date, end_date)
# 		for item in dataframe: # use reversed(dataframe) to sort reverse
# 			for x in item.values():
# 				print(x, end='	') # equal to item[x] without values()
# 			print()

# when return dataframe
	if get_trans_data(crop_codes[0], markets[0],start_date,end_date):
		
		title()

		for crop_code in crop_codes:
			for market in markets:
				gtd = get_trans_data(crop_code, market, start_date, end_date)
				for item in gtd:
					for rows in item:
						print(rows, end='	')
					print()
				print('-' * 87)

	else:
		print('查無資料！')