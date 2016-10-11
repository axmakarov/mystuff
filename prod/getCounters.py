# -*- coding: utf-8 -*-
import requests
import json

def getMetrikaTokenByUserData(username,password): # Получаем авторизационный токен для логина и пароля
	app_id = '227622dc0e774a89b6345c9c9497d1ee'
	app_pass = '9901fa3deba64165a8dd5151b805945e'
	payload = 'grant_type=password&username={0}&password={1}&client_id={2}&client_secret={3}'.format(username,password,app_id,app_pass)
	url = 'https://oauth.yandex.ru/token'
	r = requests.post(url, data=payload)
	try:
		response = json.loads(r.text)
		return response['access_token']
	except:
		return '-1'

Token = getMetrikaTokenByUserData('Ingate.Anna','Elena79')
print Token