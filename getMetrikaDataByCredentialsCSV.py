#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

def openMetrikaCredentialsFromFile(filename):
	data = []
	with open(filename, 'r+') as text:
		for row in text:
			credentialsString = unicode(row.replace('\n','').decode('utf-8'))
			credentialsList = credentialsString.split(';')
			domain = credentialsList[0]
			token = credentialsList[1]
			counterID = credentialsList[2]
			credentials = dict([('domain',domain),('token',token),('counterID',counterID)])
			data.append(credentials)
	return data

def getMetrikaCSVData(credentials,params,offset):
	metrikaRequestParams = params
	metrikaRequestParams['oauth_token'] = credentials['token']
	metrikaRequestParams['ids'] = credentials['counterID']
	metrikaRequestParams['offset'] = str(offset)
	metrikaRequestParams['limit'] = str(10000)
	# if not params['filters']:
	# 	del(params['filters'])
	metrikaRequestParams = dict((k, v) for k, v in metrikaRequestParams.iteritems() if v)
	payload = []
	for k,v in metrikaRequestParams.items():
		payload.append('{0}={1}'.format(k,v))
	url = "https://beta.api-metrika.yandex.ru/stat/v1/data.csv?"+'&'.join(payload)
	url = url.decode('utf-8')
	r = requests.get(url)
	return r.text
	# metrikaRequestParams2 = ''
	# for k,v in metrikaRequestParams.items():
	# 	metrikaRequestParams2 = metrikaRequestParams2 + '{0}={1}'.format(k,v)
	# 	metrikaRequestParams2 = metrikaRequestParams2 + '&'
	# payload = []
	# for k,v in metrikaRequestParams.iteritems():
	# 	payload.append('{0}={1}'.format(k,v))
	# print '&'.join[payload]
	# r = requests.get("https://beta.api-metrika.yandex.ru/stat/v1/data.csv", params=metrikaRequestParams)
	# print r.url


def createMetrikaRequestParams(dimensions,metrics,date1,date2,filters):
	metrikaRequestParams = dict([('dimensions',dimensions),('metrics',metrics),('date1',date1),('date2',date2),('filters',filters)])
	return metrikaRequestParams


credentials = openMetrikaCredentialsFromFile('D:\\dev-trash\\projects17out.txt')

dimensions = ''
metrics = 'ym:s:visits'
date1 = '2014-05-01'
date2 = '2015-05-31'
filters = ""
params = createMetrikaRequestParams(dimensions,metrics,date1,date2,filters)

f1 = open ('D:\\dev-trash\\output18.txt', 'w+')

count = len(credentials)
i = 0

for credential in credentials:
	i += 1
	print '{0} из {1}: Получаем данные для {2}'.format(i,count,credential['domain'].encode('utf-8')).decode('utf-8')
	data = getMetrikaCSVData(credential,params,1).encode('utf-8')
	for row in data.split('\n'):
		if row != '\n' and row != '' and not ('Итого и средние' in row):
			print >>f1, '"{0}",{1}'.format(credential['domain'].encode('utf-8'),row)

# https://beta.api-metrika.yandex.ru/stat/v1/data.csv?dimensions=ym:s:lastTrafficSource,ym:s:lastAdvEngine,ym:s:UTMSource,ym:s:UTMMedium&metrics=ym:s:visits&oauth_token=21c635d052bf43c388dba5e6af956038&ids=6905371&limit=10000&offset=1&include_undefined=True&accuracy=high&date1=2014-05-06&date2=2015-05-06&filters=ym:s:UTMSource!='cubo' AND ym:s:UTMSource!='rookee'

