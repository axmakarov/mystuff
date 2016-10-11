#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
dataStampPrint = True
dateStamp = '2015-04-20'
if not dataStampPrint:
	dataStampPrint=''
f1 = open ('D:\\dev-trash\\metrikadomains.txt', 'r+')
f2 = open ('D:\\dev-trash\\parsedmetrikadomains.txt', 'w+')
for line in f1:
	x = line.split(';')
	x[2] = x[2].replace('\n','')
	url = 'https://beta.api-metrika.yandex.ru/stat/v1/data?ids='+x[2]+'&dimensions=ym:s:UTMContent,ym:s:UTMMedium&metrics=ym:s:visits,ym:s:bounceRate&limit=10000&offset=1&oauth_token='+x[1]+'&date1=2015-04-11&date2=2015-04-19'
	r = requests.get(url)
	f1 = open('D:\\dev-trash\\'+x[0].decode('utf-8')+'.json', 'w+')
	print >>f1, r.text
	print >>f2, url