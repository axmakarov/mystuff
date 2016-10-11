# -*- coding: utf-8 -*-
import json
import requests
import math

def getMetrikaData(credentials,params,offset,limit): # Получаем данные из Метрики
	metrikaRequestParams = params
	metrikaRequestParams['oauth_token'] = credentials['token']
	metrikaRequestParams['ids'] = credentials['counterID']
	metrikaRequestParams['offset'] = str(offset)
	metrikaRequestParams['limit'] = str(limit)
	metrikaRequestParams = dict((k, v) for k, v in metrikaRequestParams.iteritems() if v)
	payload = []
	for k,v in metrikaRequestParams.items():
		payload.append('{0}={1}'.format(k,v))
	url = "https://beta.api-metrika.yandex.ru/stat/v1/data?"+'&'.join(payload)
	url = url.decode('utf-8')
	r = requests.get(url)
	return json.loads(r.text)

def createMetrikaRequestParams(dimensions,metrics,date1,date2,filters): # Создает параметры реквеста к Метрике
	metrikaRequestParams = dict([('dimensions',dimensions),('metrics',metrics),('date1',date1),('date2',date2),('filters',filters)])
	return metrikaRequestParams

def getAllMetrikaData(credentials,params): # Получаем все данные из Метрики с учетом total_rows
	data = getMetrikaData(credentials,params,1,1) # Делаем запрос, чтобы понять сколько total_rows

	if 'data' in data.keys(): # Если с запросом всё ок, то делаем реквесты, чтобы вытащить все данные
		isGettingSuccess = True
		totalRows = data['total_rows']
		print 'Всего запрос возвращает {0} строк'.format(totalRows)
		requestsCount = int(math.ceil(float(totalRows)/10000.0))
		print 'Будем делать {0} запросов к API Метрики'.format(requestsCount)
		datas = []
		for i in xrange(0,requestsCount): # Получаем данные, итерационно увеличивая offse
			print 'Делаем запрос {0} из {1}'.format(i+1,requestsCount)
			try:
				data = getMetrikaData(credentials,params,i*10000+1,10000)
				if 'data' in data.keys():
					print 'Успешно получили данные'
					datas.append(data)
			except:
				print 'Ошибка получения данных в ходе запроса {0}'.format(i+1)
				continue
		if len(datas) == requestsCount:
			print 'Данные из метрики получены полностью'
		else:
			print 'Данные из метрики получили не полностью'
	else:
		isGettingSuccess = False
		print 'Ошибка получения данных'
		print data
		return 0

	if isGettingSuccess:
		dataDictionaryList = []
		for data in datas:
			for row in data['data']:
				i = 0
				rowDictionary = {}
				for dimension in row['dimensions']:
					rowDictionary[data['query']['dimensions'][i]] = dimension['name']
					i += 1
				i = 0
				for metric in row['metrics']:
					rowDictionary[data['query']['metrics'][i]] = metric
					i += 1
					rowDictionary['domain'] = credentials['domain']
				dataDictionaryList.append(rowDictionary)
		if len(dataDictionaryList) == totalRows:
			print 'Получили все {0} строк по запросу'.format(totalRows)
		else:
			print 'Получили не все строки по запросу'
		return dataDictionaryList


# credentials = dict([('domain','doorlock.ru'),('token','3af7df280769490d8322386fbfbba499'),('counterID','36936')])

# dimensions = 'ym:s:lastSearchPhrase'
# metrics = 'ym:s:visits,ym:s:pageviews'
# date1 = '2014-06-01'
# date2 = '2015-06-30'
# filters = "ym:s:lastTrafficSourceName=='Переходы из поисковых систем'"
# params = createMetrikaRequestParams(dimensions,metrics,date1,date2,filters)

