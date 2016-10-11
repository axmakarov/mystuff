#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import uuid
f1 = open('D:\\results.txt', 'w+')

params = []
queries = ['1с торговля и склад']
near = 'Москва'
for query in queries:
	data = dict([('zone', 'ru'), ('language', 'ru'), ('near', near.decode('utf-8')), ('query', query.decode('utf-8'))])
	dataItem = {'data': data}
	params.append(dataItem)

uid = str(uuid.uuid1())
payload = {"jsonrpc":"2.0","method":"getQueue","params":{"token":"2b4298c7-ac6c-11e4-8222-50465d9ff9a8","method":"getGooglePosition","params":params},"id":uid}
payload = json.dumps(payload)
print >>f1, payload