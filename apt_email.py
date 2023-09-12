# -*- coding: utf-8 -*-
#
import os, sys
import time
import base64
from farm_trans_data import days_ago, price_list_html
from send_tools import send_gmail
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

try:
	gmail_pwd = os.environ['SUVONE_PWD_ENCODE']
except KeyError:
	sys.exit('SUVONE_PWD_ENCODE is not defined!')

gmail_addr = 'suvone@gmail.com'
gmail_pwd = str(base64.b64decode(os.environ['SUVONE_PWD_ENCODE']), 'utf-8')
to_addrs = 'Kenji<kenjiliu@gmail.com>'

today = days_ago(0)
ndays_ago = days_ago(2)
now_time = time.strftime("%H:%M:%S")
day_time = time.strftime("%Y-%m-%d %H:%M:%S")
end_info = '交易日期：{}'.format(today)

crop_code = 'G3'
markets = ['台北一', '台北二']

items_list = price_list_html(crop_code, markets)		

if items_list != []:
	#ifttt_to_line('get_avocado_price', Authorization_code, items_list[0], items_list[1], end_info)

	#msg_text = '今日酪梨市場價格（{}）：\n市場別 | 上價 | 中價 | 下價 | 平均價 | 交易量\n{}\n{}'.format(today, items_list[0], items_list[1])
	msg_html = """
	<html>
	<head>
	  <meta charset="utf-8">
	</head>
	<body style="color: #000033;">
      <div style="font-size: medium;">
	  <h5>今日酪梨市場價格（{0}）：</h5>
	  <table style="background-color: grey; border-spacing: 1px; font-size: medium;">
	    <thead>
	        <tr style="background-color: lightblue;">
	        <th style="padding: 10px;">市場別</th>
	        <th style="padding: 10px;">上價</th>
	        <th style="padding: 10px;">中價</th>
	        <th style="padding: 10px;">下價</th>
	        <th style="padding: 10px;">平均價</th>
	        <th style="padding: 10px;">交易量</th>
	      </tr>
	    </thead>
	    <tbody>
	      {1}{2}
	    </tbody>
	  </table>
	  <p>更多資料：<a href="https://amis.afa.gov.tw/main/Main.aspx" style="text-decoration: none;">農產品批發市場交易行情站</a></p>
	  </div>
	</body>
	</html>""".format(today, items_list[0], items_list[1])

	#mime_text = MIMEText(msg_text, 'plain', 'utf-8')    #←建立 MIMEText 物件
	mime_text = MIMEText(msg_html, 'html', 'utf-8')
	mime_text['Subject'] = '今日酪梨市場價格({})'.format(today)
	mime_text['From'] = gmail_addr
	mime_text['To'] = to_addrs
	#mime_text['Cc'] = '副本收件者'
	mime_text = mime_text.as_string()    #←轉為字串
	#print(msg_html)
	send_gmail(gmail_addr, gmail_pwd, to_addrs, mime_text)   #←寄出郵件
	print('{} Send Successful! @{}'.format(today, day_time))
	
else:
	print('Dataless, Try again later!', now_time)