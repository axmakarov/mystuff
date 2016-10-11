#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

def getMetrikaTokenByUserData(username,password): # Получаем авторизационный токен для логина и пароля
	app_id = 'c18a1f5f82734c9f8c1312ee0b7ef6dd'
	app_pass = 'd7848b50fa144d97b64fd15c5a8ba442'
	payload = 'grant_type=password&username={0}&password={1}&client_id={2}&client_secret={3}'.format(username,password,app_id,app_pass)
	url = 'https://oauth.yandex.ru/token'
	r = requests.post(url, data=payload)
	try:
		response = json.loads(r.text)
		return response['access_token']
	except:
		return '-1'

def getMetrikaCountersByToken(oAuthToken): # Получаем массив словарей со списком счетчиков для токена
	url = 'http://api-metrika.yandex.ru/counters.json?oauth_token={0}'.format(oAuthToken)
	r = requests.get(url)
	try:
		response = json.loads(r.text)
		counters = response['counters']
		return counters
	except:
		return '-1'

def getMetrikaCounterIDByDomain(counters, domain): # Получаем ID счетчика для домена
	counterID = []
	for counter in counters:
		if domain in counter['site'] and counter['code_status'] == 'CS_OK':
			counterID.append(counter['id']) 
	return counterID

def getMetrikaCredentialsByLPD (LPD): # Получаем credentials (токен и ID счетчика) для LPD (словаря с логином, паролем и доменом)
	token = getMetrikaTokenByUserData(LPD['yandexLogin'],LPD['yandexPassword'])
	if token != '-1':
		countersList = getMetrikaCountersByToken(token)
		counterID = getMetrikaCounterIDByDomain (countersList,domain)
		metrikaCredentials = dict([('Token',token),('counterID',counterID)])
		return metrikaCredentials
	else:
		print 'Invalid login or password'

yandexLogin = 'tsvetoff.r'
yandexPassword = '.KBZ17021984'
domain = u'цветофф.рф'
LPD = dict([('yandexLogin',yandexLogin),('yandexPassword',yandexPassword),('domain',domain)])
print getMetrikaCredentialsByLPD(LPD)


# Token = getMetrikaTokenByUserData(yandexLogin,yandexPassword)
# if Token != '-1':
# 	countersList = getMetrikaCountersByToken(Token)
# 	print getMetrikaCounterIDByDomain(countersList,domain)[0]
# else:
# 	print 'Invalid login or password'


