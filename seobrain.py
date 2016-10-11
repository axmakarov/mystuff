#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import uuid
f = open('D:\\json.txt', 'w+')
f1 = open('D:\\results.txt', 'w+')

params = []
queries = ['купить телевизор', 'купить телефон', 'купить холодильник']
near = 'Москва'
for query in queries:
	data = dict([('zone', 'ru'), ('language', 'ru'), ('near', near.decode('utf-8')), ('query', query.decode('utf-8'))])
	dataItem = {'data': data}
	params.append(dataItem)

uid = str(uuid.uuid1())
payload = {"jsonrpc":"2.0","method":"getQueue","params":{"token":"2b4298c7-ac6c-11e4-8222-50465d9ff9a8","method":"getGooglePosition","params":params},"id":uid}
payloadjson = json.dumps(payload)


r = requests.post("http://parser.seobrain.ru/api", data=json.dumps(payload))
k = json.loads(r.text)
queueId = k['result']['id']
payload = {"jsonrpc":"2.0","method":"getQueueResult","params":{"token":"2b4298c7-ac6c-11e4-8222-50465d9ff9a8","id":queueId},"id":uid}
r = requests.post("http://parser.seobrain.ru/api", data=json.dumps(payload))
#k = json.loads(r.text)
k = (r.text).encode('utf-8')
print >>f, k
d = json.loads(r.text)
d = d['result']
for item in d:
	query1 = item['request']['data']['query']
	print >>f1, query1.encode('utf-8')