#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
file1 = open('D:\\queryexample.txt', 'w+')
data = []
queries = ['купить телевизор', 'купить телефон']
for query in queries:
	k = dict([('zone', 'ru'), ('language', 'ru'), ('near', 'Москва'.decode('utf-8')), ('query', query.decode('utf-8'))])
	k1 = {'data': k}
	data.append(k1)
payload = {"jsonrpc":"2.0","method":"getQueue","params":{"token":"2b4298c7-ac6c-11e4-8222-50465d9ff9a8","method":"getGooglePosition","params":data},"id":"123"}
print >>file1, payload