#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import csv
import sys
import uuid
# Опрашиваем много счетчиков метрики и выгружаем всю хуйню в CSV

f1 = open ('D:\\dev-trash\\detstr.txt', 'r+')
f3 = open ('D:\\dev-trash\\metrikafullresults2.txt', 'w+')
f4 = open ('D:\\dev-trash\\domainuids.txt', 'w+')
# for row in csvreader:
	# print u'Сайт: {0}; Токен: {1}; ID счетчика: {2}'.format(row[0], row[1], row[2])

i = 0
for row in f1:
	i += 1
	x = row.split(';')
	x[2] = x[2].replace('\n','')
	date1 = 'date1=2014-05-06'
	date2 = 'date2=2015-05-06'
	limit = 'limit=10000'
	oAuthToken = 'oauth_token='+x[1]
	counterID = 'id='+x[2]
	dimensions = 'dimensions='+'ym:s:lastTrafficSource,ym:s:lastAdvEngine,ym:s:UTMSource,ym:s:UTMMedium'
	metrics = 'metrics='+'ym:s:visits,ym:s:pageviews,ym:s:bounceRate,ym:s:avgVisitDurationSeconds,ym:s:sumGoalReachesAny'
	filters = 'filters='+"ym:s:UTMSource!='cubo' AND ym:s:UTMSource!='rookee'"
	url = "https://beta.api-metrika.yandex.ru/stat/v1/data.csv?"+'&'.join([oAuthToken,counterID,dimensions,metrics,filters,date1,date2,limit])
	# print url.decode('utf-8')
	print '{0} - {1}'.format(i,x[0].decode('cp1251'))
	uid = str(uuid.uuid1())
	print >>f4, "{0};{1}".format(uid,x[0])
	# a = row[0].('utf-8')
	# enc = chardet.detect(row[0].decode('utf-8'))
	# print enc['confidence']
	# print enc['encoding']
	# print row[0].replace('.','-').decode('utf-8').encode('cp1251')
	r = requests.get(url)
	# print sys.getfilesystemencoding()
	f2 = open('D:\\dev-trash\\metrika-csv\\'+x[0]+'.txt', 'w+')
	d = r.text.encode('utf-8')
	d = d.split('\n')
	j = 0
	for data in d:
		if data != '\n' and data != '':
			print>>f3, '"{0}",'.format(uid)+data
			j += 1
	if j > 10000:
		print 'Rows greater than 10000'
	print >>f2, r.text.encode('utf-8')
# url = "https://beta.api-metrika.yandex.ru/stat/v1/data.csv?metrics=ym:s:visits,ym:s:pageviews,ym:s:bounceRate,ym:s:avgVisitDurationSeconds&dimensions=ym:s:lastTrafficSource,ym:s:lastAdvEngine,ym:s:UTMSource&limit=10000&date1=2014-04-22&date2=2015-04-22&filters=(ym:s:lastTrafficSourceName=='Переходы по рекламе') AND ym:s:UTMSource!='cubo' AND ym:s:UTMSource!='rookee'&id=625906&oauth_token=8c6f86d870014c1aaeff3e53fea163e6"
# r = requests.get(url)
# f2 = open('D:\\dev-trash\\resultsmetrika.txt', 'w+')
# print >>f1, r.text.encode('utf-8')
