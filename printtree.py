#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
jsonPath = 'D:\\jsonfolder\\'
resultPath = 'D:\\dev-trash\\result.txt'
resultFile = open (resultPath, 'w+')
print >>resultFile, '{0};{1};{2};{3};{4}'.format ('project', 'utm_content', 'utm_source', 'visits', 'bounceRate')
for d, dirs, files in os.walk(jsonPath):
	for f in files:
		currentJsonFile = open (jsonPath+str(f), 'r+')
		data = json.load(currentJsonFile)
		# resultFile = open ('D:\\dev-trash\\'+'data-'+str(f).replace('json','txt'), 'w+')
		for item in data['data']:
			print >>resultFile, '{0};{1};{2};{3};{4}'.format (str(f).replace('.json',''), item['dimensions'][0]['name'], item['dimensions'][1]['name'], item['metrics'][0], item['metrics'][1])
