#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
dataListPath = 'D:\\dev-trash\\fulldomainlist.txt'
outDataList = open ('D:\\dev-trash\\outdatalist.txt', 'w+')
dataListFile = open (dataListPath, 'r+')
itemsCountInDataListFile = 0
for item in dataListFile:
	itemsCountInDataListFile += 1
print 'Количество входных записей = {0}'.format(itemsCountInDataListFile).decode('utf-8')
dataListFile.seek(0)
if itemsCountInDataListFile > 0:
	itemList = []
	for item in dataListFile:
		valuesList = item.split(';')
		valuesList[4] = valuesList[4].replace('\n','')
		itemList.append(valuesList)
	print >>outDataList, itemList
	itemCounter = 0
	for item in itemList:
		itemCounter += 1
		print 'Обрабатываем входную запись #{0} из {1}'.format(itemCounter, itemsCountInDataListFile).decode('utf-8')
		itemName = item[0]
		oauthToken = item[1]
		counterId = item[2]
		date1 = item[3]
		date2 = item[4]
		try:
			itemName = unicode(itemName.decode('cp1251'))
		except:
			print 'Нихера'
		# print >>outDataList, '\n{0} ; {1} ; {2} ; {3} ; {4}'.format(itemName,oauthToken,counterId,date1,date2)
		url = "https://beta.api-metrika.yandex.ru/stat/v1/data?ids="+counterId+"&dimensions=ym:s:lastSourceEngine,ym:s:date&metrics=ym:s:visits&oauth_token="+oauthToken+"&date1="+date1+"&date2="+date2+"&filters=ym:s:lastTrafficSourceName=='Переходы из поисковых систем'&limit=10000&offset=1&sort=ym:s:date"
		r = requests.get(url)
		print u'Получили данные по API для {0}'.format(itemName)
		outJsonFilePath = 'D:\\dev-trash\\metrika-json\\'+unicode(itemName)+'.json'
		outJsonFile = open (outJsonFilePath, 'w+')
		print >>outJsonFile, r.text.encode('utf-8')
		print u'Записали данные в файл {0}'.format(outJsonFilePath)



#oauthToken = '21c635d052bf43c388dba5e6af956038'
#counterId = '8306167'
#date1 = '2014-01-01'
#date2 = '2015-04-20'
#url = "https://beta.api-metrika.yandex.ru/stat/v1/data?ids="+counterId+"&dimensions=ym:s:lastSourceEngine,ym:s:date&metrics=ym:s:visits&oauth_token="+oauthToken+"&date1="+date1+"&date2="+date2+"&filters=ym:s:lastTrafficSourceName=='Переходы из поисковых систем'&limit=10000&offset=1&sort=ym:s:date"
#r = requests.get(url)
#f1 = open ('D:\\dev-trash\\metrika.json', 'w+')
#print >>f1, r.text.encode('utf-8')

