#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Send message to Line Notify
#
import os
import sys
import time
import requests
from farm_trans_data import days_ago, price_list
from send_tools import send_line_notify
from check_log import checklog
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
	try:
		token = os.environ['GAP_LINE_TOKEN']
	except KeyError:
		sys.exit('GAP_LINE_TOKEN is not defined!')

	self_name = os.path.basename(__file__).split('.')[0]
	log_name = '/tmp/{}.log'.format(self_name)
	today = days_ago(0)
	ndays_ago = days_ago(2)
	now_time = time.strftime("%H:%M:%S")
	day_time = time.strftime("%Y-%m-%d")

	log = open('/tmp/{}.log'.format(self_name), 'a')

	if not checklog(log_name):
		
		title = '市場別 | 上價 | 中價 | 下價 | 平均價 | 交易量'
		crop_code = ['G3']
		markets = ['台北一', '台北二']
		
		items_list = price_list(crop_code, markets)
		message = '\n交易日期：{}\n\n{}\n{}\n{}\n\n@{}'.format(today, title, items_list[0], items_list[1], day_time)

		status_code = send_line_notify(token, message)

		if status_code == 200:
			log.write('{} Send Successful! @{}\n'.format(today, now_time))
			print('{} Send Successful! @{} {}'.format(today, day_time, now_time))
			# print('status_code =', status_code)
			# print(token)
			# print(message)
			log.close()
		else:
			print('Oh, There is something wrong!')
	else:
		log.write('Today have already sent, will not send again. @{}\n'.format(now_time))
		print('Today have already sent, will not send again. @{}'.format(now_time))
		log.close()
