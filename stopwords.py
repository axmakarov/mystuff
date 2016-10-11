#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Создает тело запроса к seozoo для опроса вордстата
import json

file1 = open('D:\\dev-trash\\stopwords.txt','r+') # Запросы (кодировка ANSI, разделитель \n)
file2 = open('D:\\dev-trash\\stopwordsresult.txt','w+') # Ответ: тело запроса
params2 = []
for line in file1:
	line = line.replace ('\n','')
	dict1 = dict([('phrase',line.decode('cp1251')),('page','1')])
	dict2 = dict([('data',dict1)])
	params2.append(dict2)
params1 = dict([('token','UH7ForyW2o2QGIruyktzXbiivQ89EsEK197Ioccc'),('method','getWordstat'),('params',params2)])
request = dict([('jsonrpc','2.0'),('method','getQueue'),('params',params1),('id',123)])
request = json.dumps(request)

print >>file2, request