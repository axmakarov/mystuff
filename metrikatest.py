#!/usr/bin/env python
# -*- coding: utf-8 -*-
import metrikaHelper

def openLPDFromFile(filename):
	data = []
	with open(filename, 'r+') as text:
		for row in text:
			LPDString = unicode(row.replace('\n','').decode('cp1251'))
			LPDList = LPDString.split(';')
			yandexLogin = LPDList[1].replace('@yandex.ru','')
			yandexPassword = LPDList[2]
			domain = LPDList[0]
			LPD = dict([('yandexLogin',yandexLogin),('yandexPassword',yandexPassword),('domain',domain)])
			data.append(LPD)
	return data


LPDs = openLPDFromFile('D:\\dev-trash\\projects12.csv')
output = open('D:\\dev-trash\\projects12out.txt', 'w+')

LPDsCount = len(LPDs)
i = 0

for LPD in LPDs:
	i += 1
	print '{0} из {1}: Получаем Credentials для {2}'.format(i,LPDsCount,LPD['domain'].encode('utf-8')).decode('utf-8')
	Credentials = metrikaHelper.getMetrikaCredentialsByLPD(LPD)
	if Credentials['counterID']:
		print >>output, "{0};{1};{2}".format(LPD['domain'].encode('utf-8'),Credentials['Token'],Credentials['counterID'][0])

# yandexLogin = 'tsvetoff.r'
# yandexPassword = '.KBZ17021984'
# domain = u'цветофф.рф'
# LPD = dict([('yandexLogin',yandexLogin),('yandexPassword',yandexPassword),('domain',domain)])
# print metrikaHelper.getMetrikaCredentialsByLPD(LPD)
