#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urlparse import urlparse
f1 = open('D:\\result.json', 'r')
f2 = open('D:\\textresult.txt', 'w+')
text = json.load(f1)
d = text['result']
for item in d:
	query1 = item['request']['data']['query']
	print >>f2, query1.encode('utf-8')
	e = item['response']['results']
	for item2 in e:
		url = item2['url']
		parsed_uri = urlparse(url)
		domain = '{uri.netloc}'.format(uri=parsed_uri)
		print >>f2, url.encode('utf-8')+"\t"+domain.encode('utf-8')
