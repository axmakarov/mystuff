# -*- coding: utf-8 -*-
import random
import json

f1 = open ('D:\\dev-trash\\rtbstat.json', 'w+')
f2 = open ('D:\\dev-trash\\rtbstat2.txt', 'w+')

# Создаем статистику
i = random.randint (15,30)
counter = 1
domains = []
while counter <= i:
	domainId = counter
	themes = dict([('theme1',random.random()),('theme2',random.random()),('theme3',random.random()),('theme4',random.random())])
	domain = dict([('domainId',domainId),('themes',themes)])
	domains.append(domain)
	counter += 1
print domains[-1]
print i
dayList = []
days = random.randint (15,45)
counter = 1
while counter <= days:
	visitsCount = random.randint (i,i*2)
	counter2 = 0
	visitedDomains = []
	while counter2 <= visitsCount:
		visitedDomain = random.choice (domains)
		visitedDomains.append(visitedDomain)
		counter2 += 1
	dayItem = dict([('dayCount',counter),('visitedDomains',visitedDomains)])
	dayList.append(dayItem)
	counter += 1

jsonFile = json.dumps(dayList)
print >>f1, jsonFile

for day in dayList:
	for visit in day['visitedDomains']:
		print >>f2, '{}\t{}\t{}\t{}\t{}\t{}'.format(day['dayCount'],visit['domainId'],visit['themes']['theme1'],visit['themes']['theme2'],visit['themes']['theme3'],visit['themes']['theme4'])

