#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

def getMetrikaData (data, name):
	if data['data']:
		for item in data['data']:
			lastSourceEngine = item['dimensions'][0]['name'].encode('utf-8')
			lastSourceEngineId = item['dimensions'][0]['id'].encode('utf-8')
			date = item['dimensions'][1]['name'].encode('utf-8')
			visits = item['metrics'][0]
			print >>resultFile, '{0};{1};{2};{3};{4}'.format (name, lastSourceEngine, lastSourceEngineId, date, visits)


jsonPath = 'D:\\dev-trash\\metrika-json\\'
resultPath = 'D:\\dev-trash\\result.txt'
resultWithTotalRowsPath = 'D:\\dev-trash\\totalrowsinfiles.txt'
totalRowsFile = open(resultWithTotalRowsPath, 'w+')
resultFile = open (resultPath, 'w+')
fileList = open ('D:\\dev-trash\\filelist.txt', 'w+')
print >>resultFile, '{0};{1};{2};{3};{4}'.format ('project', 'lastSourceEngine', 'lastSourceEngineId', 'date', 'visits')
jsonFilesPaths = []
for d, dirs, files in os.walk(jsonPath):
	for f in files:
		currentPath = jsonPath+str(f)
		print >>fileList, currentPath
		jsonFilesPaths.append (currentPath)
totalFilesCount = len(jsonFilesPaths)
print u'Всего JSON-файлов на входе: {0}'.format(totalFilesCount)

fileCounter = 0
for jsonFilePath in jsonFilesPaths:
	fileCounter += 1
	print u'Обрабатываем файл #{0} {1} из {2}'.format(fileCounter,jsonFilePath.decode('cp1251'),totalFilesCount)
	currentJsonFile = open(jsonFilePath, 'r+')
	try:
		data = json.load(currentJsonFile)
	except:
		print u'Не удается прочитать JSON из файла {0}'.format(jsonFilePath.decode('cp1251'))
		continue
	if 'data' in data:
		name = jsonFilePath.replace(jsonPath,'').replace('.json','').decode('cp1251').encode('utf-8')
		print >>totalRowsFile, '{0};{1}'.format(name,data['total_rows'])
		getMetrikaData (data, name)
		print u'Записали данные в results.txt'
	elif 'errors' in data:
		print u'Ошибка в ответе Метрики: {0}'.format(data['code'])
	else:
		print u'Неизвестная ошибка'


