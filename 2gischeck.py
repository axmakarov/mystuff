# -*- coding: utf-8 -*-
import requests
import json

site = 'wikimart.ru'
r = requests.get('http://catalog.api.2gis.ru/search?what={0}&where=Москва&version=1.3&key=rudcgu3317'.format(site))
with open('D:\\dev-trash\\2gischeck\\test.txt', 'w+') as f1:
	print >>f1, r.text.encode('utf-8')
data = json.loads(unicode(r.text))
if 'result' in data:
	rubrics = data['result'][0]['rubrics']
for rubric in rubrics:
	print rubric