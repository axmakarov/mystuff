#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
date1 = '2015-04-11'
date2 = '2015-04-19'
f1 = open ('D:\\dev-trash\\metrikadomains.txt', 'r+')
f2 = open ('D:\\dev-trash\\parsedmetrikadomains.txt', 'w+')
lineCount = 0
for line in f1:
	lineCount += 1
f1.seek(0)
print 'Total request count = {0}'.format(lineCount)
i = 0
for line in f1:
	x = line.split(';')
	x[2] = x[2].replace('\n','')
	url = 'https://beta.api-metrika.yandex.ru/stat/v1/data?ids='+x[2]+'&dimensions=ym:s:UTMContent,ym:s:UTMMedium&metrics=ym:s:visits,ym:s:bounceRate&limit=10000&offset=1&oauth_token='+x[1]+'&date1='+date1+'&date2='+date2
	print >>f2, url
	r = requests.get(url)
	f1 = open('D:\\dev-trash\\'+x[0].decode('utf-8')+'.json', 'w+')
	print >>f1, r.text.encode('utf-8')
	i += 1
	print 'Successful data write for {0}. Progress: {1} of {2}'.format(x[0],i,lineCount)
print 'Success!'