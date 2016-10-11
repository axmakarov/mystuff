#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
jsonPath = 'D:\\dev-trash\\metrika-json\\'
resultPath = 'D:\\dev-trash\\result.txt'
resultFile = open (resultPath, 'w+')
fileList = open ('D:\\dev-trash\\filelist.txt', 'w+')
print >>resultFile, '{0};{1};{2};{3};{4}'.format ('project', 'lastSourceEngine', 'lastSourceEngineId', 'date', 'visits')
i = 0
j = 0
e = 0
for d, dirs, files in os.walk(jsonPath):
	for f in files:
		print >>fileList, f
		currentJsonFile = open (jsonPath+str(f), 'r+')
		try:
			data = json.load(currentJsonFile)
		except:
			print 'Error when read json in {0} file'.format(str(f))
			e += 1
			pass
			continue
		# resultFile = open ('D:\\dev-trash\\'+'data-'+str(f).replace('json','txt'), 'w+')
		try:
			if data['data']:
				dataItems = len(data['data'])
				currentItemNumber = 0
				for item in data['data']:
					currentItemNumber += 1
					print '{0} in {1}'.format(currentItemNumber,dataItems)
					print >>resultFile, '{0};{1};{2};{3};{4}'.format (str(f).replace('.json',''), item['dimensions'][0]['name'].decode('utf-8'), item['dimensions'][0]['id'].encode('utf-8'), item['dimensions'][1]['name'].encode('utf-8'), item['metrics'][0])
				i+=1
			else:
				j+=1
		except:
			if 'errors' in data:
				if data['errors']:
					print 'Error in response {0}: {1}'.format(str(f),data['code'])
					e += 1
				pass
print 'Total success files: {0}'.format(i)
print 'Empty json-datas: {0}'.format(j)
print 'Error files: {0}'.format(e)
