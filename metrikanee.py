#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

def getMetrikaData(credentials,params,offset):
	metrikaRequestParams = params
	metrikaRequestParams['oauth_token'] = credentials['token']
	metrikaRequestParams['ids'] = credentials['counterID']
	metrikaRequestParams['offset'] = str(offset)
	metrikaRequestParams['limit'] = str(10000)
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

credentials = dict([('domain','antonchik.ru'),('token','3c5dea1992c74e0899579105ed03cd3d'),('counterID','314293')]) # Авторизационные данные для сайта

URLLabels = ['id=at','id=y','id=kr','id=g','di=kr','id=cr','id=ct','openstat=','yclid','=atteas','=aty_j','=atg_j','=atb_j','=at','=atteas','=krd','=kry','utm'] # Перечень специальных меток, задается вручную (например, из брифа)
URLFilter = "ym:s:startURLName!~'{0}'".format('('+'|'.join(URLLabels)+')') # Из специальных меток делаем фильтр с регуляркой

BrandWords = ['антончик','antonchik'] # Перечень брендовых слов
SearchPhraseFilter = "ym:s:lastSearchPhrase!~'{0}'".format('('+'|'.join(BrandWords)+')')  # Из перечня брендовых слов делаем фильтр с регуляркой

dimensions = 'ym:s:year,ym:s:month'
metrics = 'ym:s:visits'
date2 = '2015-04-30' # Последняя дата последнего полного месяца
date1 = '2013-04-30' # date2 минус 2 года
SourceFilter = "ym:s:lastTrafficSourceName=='Переходы из поисковых систем'"
filters = ' AND '.join([SourceFilter,URLFilter,SearchPhraseFilter]) # Из всех условий фильтрации (SourceFilter,URLFilter,SearchPhraseFilter) делаем содержимое фильтра через AND
params = createMetrikaRequestParams(dimensions,metrics,date1,date2,filters)

data = getMetrikaData(credentials,params,1)

f1 = open ('D:\\dev-trash\\metrikanee.txt','w+') # 

monthTraffic = []
for row in data['data']:
	visits = int(row['metrics'][0])
	year = int(row['dimensions'][0]['name'])
	month = int(row['dimensions'][1]['name'])
	dataItem = dict([('visits',visits),('year',year),('month',month)])
	monthTraffic.append(dataItem)

print >>f1, monthTraffic




# Какой запрос должен получится: https://beta.api-metrika.yandex.ru/stat/v1/data?dimensions=ym:s:year,ym:s:month&metrics=ym:s:visits&date1=2013-04-30&date2=2015-04-30&ids=314293&oauth_token=3c5dea1992c74e0899579105ed03cd3d&limit=10000&offset=1&sort=ym:s:year&filters=ym:s:lastTrafficSourceName=='Переходы из поисковых систем' AND ym:s:startURLName!~'(id=at|id=y|id=kr|id=g|di=kr|id=cr|id=ct|openstat=|yclid|=atteas|=aty_j|=atg_j|=atb_j|=at|=atteas|=krd,=kry,utm)' AND ym:s:lastSearchPhrase!~'(антончик|antonchik)'