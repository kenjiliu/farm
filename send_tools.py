# -*- coding: utf-8 -*-
# Use tools to send message
import os
import sys
import requests
import json
import time
import smtplib

def ifttt_to_line(EventName, Authorization_code, value1, value2, value3):
    url_ifttt ='https://maker.ifttt.com/trigger/' + EventName + '/with/key/' + Authorization_code +'?'
    payload = {'value1': value1, 'value2': value2, 'value3': value3} 
    res = requests.get(url_ifttt, params=payload)  #發送請求
    return res.text

    # https://ifttt.com/applets/Gd4mh27P 
    # Setting Message:
    # <br>
    # 酪梨市場價格：<br><br>
    # 市場別 | 上價 | 中價 | 下價 | 平均價 | 交易量 <br>
    # {{Value1}}<br>
    # {{Value2}}<br><br>
    # {{Value3}}

def send_line_notify(token, msg):
	api_url = 'https://notify-api.line.me/api/notify'
	headers = {"Authorization": "Bearer " + token, "Content-Type" : "application/x-www-form-urlencoded"}
	payload = {'message': msg}
	r = requests.post(api_url, headers = headers, params = payload)
	return r.status_code
	# try:
	# 	token = os.environ['GAP_LINE_TOKEN']
	# except KeyError:
	# 	sys.exit('GAP_LINE_TOKEN is not defined!')

def send_gmail(gmail_addr, gmail_pwd, to_addrs, msg):
    """Send email from gmail's SMTP server.
    gmail_addr: gmail account
    gmail_pwd: gmail password
    to_addrs: send to email address
    msg: messages to send
    """
    smtp_gmail = smtplib.SMTP('smtp.gmail.com', 587)	# 建立 SMTP 物件
    print(smtp_gmail.ehlo())	    # Say Hello
    print(smtp_gmail.starttls())	 # 啟動 TLS 加密模式
    print(smtp_gmail.login(gmail_addr, gmail_pwd))	# 登入
    status = smtp_gmail.sendmail(gmail_addr, to_addrs, msg)	  # 寄出
    # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    #     smtp.login(gmail_addr, gmail_pwd)
    #     status = smtp.send_message(msg)
 
    if not status:
        print('Send Successful!')
    else:
        print('Send Failure!', status)
    smtp_gmail.quit()	# 結束與郵件伺服器的連線
    # smtp.quit()