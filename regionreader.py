# -*- coding: utf-8 -*-
import json
f1 = open ('D:\\dev-trash\\metrika-regions28.json', 'r+')
f2 = open ('D:\\dev-trash\\metrika-regions28.txt', 'w+')
k = json.load(f1)
data = k['data']
totalCounts = len(data)
i = 1
for dataItem in data:
	print 'Обрабатываем строку {0} из {1}'.format(i, totalCounts).decode('utf-8')
	regionCountryName = unicode(dataItem['dimensions'][0]['name'])
	regionCountryID = dataItem['dimensions'][0]['id']
	regionAreaName = unicode(dataItem['dimensions'][1]['name'])
	regionAreaID = dataItem['dimensions'][1]['id']
	regionCityName = unicode(dataItem['dimensions'][2]['name'])
	regionCityID = dataItem['dimensions'][2]['id']
	# print >>f2, '{}\t{}\t{}\t{}'.format(i,'regionCountry',regionCountryID,regionCountryName.encode('utf-8'))
	# print >>f2, '{}\t{}\t{}\t{}'.format(i,'regionArea',regionAreaID,regionAreaName.encode('utf-8'))
	# print >>f2, '{}\t{}\t{}\t{}'.format(i,'regionCity',regionCityID,regionCityName.encode('utf-8'))
	print >>f2, '{}\t{}\t{}\t{}\t{}\t{}'.format(regionCountryID,regionCountryName.encode('utf-8'),regionAreaID,regionAreaName.encode('utf-8'),regionCityID,regionCityName.encode('utf-8'))
	i += 1
