#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ifttt_ftd_to_line.py
#
import os
import sys
import time
from farm_trans_data import days_ago, price_list
from send_tools import ifttt_to_line
from check_log import checklog
from dotenv import load_dotenv

load_dotenv()

try:
	Authorization_code = os.environ['GAP_IFTTT_AUTH_CODE'] #ifttt授權碼
except KeyError:
	sys.exit('GAP_IFTTT_AUTH_CODE is not defined!')

self_name = os.path.basename(__file__).split('.')[0]
log_name = '/tmp/{}.log'.format(self_name)
today = days_ago(0)
ndays_ago = days_ago(2)
now_time = time.strftime("%H:%M:%S")
day_time = time.strftime("%Y-%m-%d")

log = open('/tmp/{}.log'.format(self_name), 'a')

if not checklog(log_name):
	end_info = '交易日期：{}'.format(today)
	crop_code = 'G3'
	markets = ['台北一', '台北二']

	items_list = price_list(crop_code, markets)		

	if items_list != []:
		ret = ifttt_to_line('get_avocado_price', Authorization_code, items_list[0], items_list[1], end_info)
		if ret[:5] == 'Congr':
			log.write('{} Send Successful! @{}\n'.format(today, now_time))
			print('{} Send Successful! @{}'.format(today, now_time))
			#print(ret)
			log.close()			
	else:
		print('Dataless, Try again later!', now_time)
else:
	log.write('Today have already sent, will not send again. @{}\n'.format(now_time))
	print('Today have already sent, will not send again. @{}'.format(now_time))
	log.close()

