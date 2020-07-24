# -*- coding: utf-8 -*-
import requests
import json
import time
import farm_trans_data as ftd

date = time.strftime("%Y.%m.%d", time.localtime())
today = ftd.xiyuan_to_minguo(date, '.')
#print(today)

columns = ['交易日期', '作物代號', '作物名稱', '市場代號', '市場名稱', '上價', '中價', '下價', '平均價', '交易量']

print('今日酪梨市場交易價格：')
print('-' * 48)
for i in range(4, len(columns)):
	print(columns[i], end='  ')
print()
print('-' * 48)

# 想要的品種
crops = ['G3']
# 想要的市場
markets = ['台北一', '台北二']

for market in markets:
	data = ftd.get_trans_data(crops, market, today)
	for item in data:
		for rows in range(4,len(item)):
			print(item[rows], end='	')
		print()
	print('-' * 48)
