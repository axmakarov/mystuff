# -*- coding: utf-8 -*-
import json
inputFile = open('D:\\dev-trash\\merge_major-r.ru.json', 'r+')
outputFile = open('D:\\dev-trash\\queries_major-r.ru.txt', 'w+')
data = json.load(inputFile)
for dataItem in data:
	print >>outputFile, '{0}\t{1}'.format(dataItem['Text'].encode('utf-8'),dataItem['Weight'])