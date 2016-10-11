# -*- coding: utf-8 -*-
import json
from collections import defaultdict

data2 = []
with open ('D:\\wordstat.csv','r+') as text:
	for row in text:
		dataItem = unicode(row.replace('\n','').decode('cp1251'))
		dataList = dataItem.split(';')
		keyword = dataList[2]
		month = dataList[0][3:5]
		year = dataList[0][6:10]
		impressions = dataList[1]
		item = dict([('keyword',keyword.encode('utf-8')),('month',month),('year',year),('impressions',int(impressions))])
		data2.append(item)

with open ('D:\\wordstatlist.json','w+') as f1:
	print >>f1, json.dumps(data2)

c = defaultdict(int)
for d in data2:
	d['m-y'] = d['month']+'-'+d['year']
	c[d['m-y']] += d['impressions']

with open ('D:\\wordstatsum.txt','w+') as f2:
	print >>f2, c


