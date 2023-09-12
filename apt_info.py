# -*- coding: utf-8 -*-
import requests
import json
import time
import farm_trans_data as ftd

today = ftd.days_ago(0)
ndays_ago = ftd.days_ago(2)
now_time = time.strftime("%H:%M:%S")
day_time = time.strftime("%Y-%m-%d %H:%M:%S")
#print(today)

columns = ['交易日期', '種類代碼', '作物代號', '作物名稱', '市場代號', '市場名稱', '上價', '中價', '下價', '平均價', '交易量']

def print_title():
	print('【酪梨】市場價格 ({})'.format(today))
	print('-' * 48)
	for i in range(5, len(columns)):
		if i == (len(columns) - 1):
			print(columns[i], end='')
		else:
			print(columns[i], end=' | ')
			i += 1		
	print()
	print('-' * 48)

# 作物代碼
crop_code = ['G3']

# 市場名稱
markets = ['台北一', '台北二', '台中市', '高雄市']

def main():
	print_title()
	contents = ftd.price_list(crop_code, markets)
	for item in contents:
		print(item)

	# for market in markets:
	# 	if ftd.check_market_rest(market, ndays_ago):
	# 		print('{}	[本日休市]'.format(market))
	# 	else:
	# 		data = ftd.get_trans_data(crop_code, market, ndays_ago, ndays_ago)
	# 		if data:
	# 			for item in data:
	# 				i = item.index(market)
	# 				for rows in range(i, len(item)):
	# 					if i == (len(item) - 1):
	# 						print(item[rows], end='')
	# 					else:
	# 						print(item[rows], end=' | ')
	# 						i += 1				
	# 			print()
	# 		else:
	# 			print('{}	[本日尚無資料] {}'.format(market, now_time))

	print('-' * 48)	
	print('查詢時間：{}'.format(day_time))	

if __name__ == '__main__':
	main()
