# -*- coding: utf-8 -*-
import json
import requests
f1 = open('D:\\dev-trash\\logins4direct2.txt','r+')
data = []
with f1 as text:
	for row in text:
		dataString = row.replace('\n','')
		dataList = dataString.split(';')
		yandexLogin = dataList[0]
		yandexPassword = dataList[1]
		yandexAcc = dict([('yandexLogin',yandexLogin),('yandexPassword',yandexPassword)])
		data.append(yandexAcc)
f2 = open('D:\\dev-trash\\logins4directoutput2.txt','w+')
app_id = '66e100851f714c13ada9e3248e32c77a'
app_pass = '147c606574c14134a0280b7d9aa8e0a2'
i = 1
for Account in data:
	print ('{} account').format(i)
	payload = 'grant_type=password&username={0}&password={1}&client_id={2}&client_secret={3}'.format(Account['yandexLogin'],Account['yandexPassword'],app_id,app_pass)
	url = 'https://oauth.yandex.ru/token'
	r = requests.post(url, data=payload)
	try:
		response = json.loads(r.text)
		print >>f2, '{0}\t{1}\t{2}'.format(Account['yandexLogin'],Account['yandexPassword'],response['access_token'])
	except:
		print 'error'
	i += 1


