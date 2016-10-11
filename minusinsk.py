# -*- coding: utf-8 -*-
import lxml.html

with open('D:\\dev-trash\\shortminus.csv','r+') as text:
	for row in text:
		rowString = unicode(row.replace('\n','').decode('utf-8'))
		rowList = rowString.split(';')
		if rowList[0] == 'domain':
			continue
		url = 'http://'+rowList[0]
		try:
			t = lxml.html.parse(url)
			print t.find(".//title").text
		except:
			print 'lxml error'
		print rowList[0].encode('utf-8')
		