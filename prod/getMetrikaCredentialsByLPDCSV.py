#!/usr/bin/env python
# -*- coding: utf-8 -*-
import metrikaHelper

def openLPDFromFile(filename): # Открываем файл со списком LPD (логин-пароль-домен, структура данных: домен;логин;пароль, кодировка ANSI) и возвращаем LPD в виде массива словарей
	data = []
	with open(filename, 'r+') as text:
		for row in text:
			LPDString = unicode(,..decode('cp1251'))
			LPDList = LPDString.split(';')
			yandexLogin = LPDList[1].replace('@yandex.ru','')
			yandexPassword = LPDList[2]
			domain = LPDList[0]
			LPD = dict([('yandexLogin',yandexLogin),('yandexPassword',yandexPassword),('domain',domain)])
			data.append(LPD)
	return data


LPDs = openLPDFromFile('D:\\dev-trash\\projects15.csv')
output = open('D:\\dev-trash\\projects15out.txt', 'w+')

LPDsCount = len(LPDs) # Подсчитываем количество словарей LPD в массиве
i = 0

for LPD in LPDs:
	i += 1
	print '{0} из {1}: Получаем Credentials для {2}'.format(i,LPDsCount,LPD['domain'].encode('utf-8')).decode('utf-8')
	try:
		Credentials = metrikaHelper.getMetrikaCredentialsByLPD(LPD)
		if Credentials['counterID']:
			print >>output, "{0};{1};{2}".format(LPD['domain'].encode('utf-8'),Credentials['Token'],Credentials['counterID'][0])
	except:
		pass