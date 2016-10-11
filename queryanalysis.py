# -*- coding: utf-8 -*-
import locale
import re
locale.setlocale(locale.LC_ALL, '')
russianAlphabet = ['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']
englishAlphabet = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w']
queries = []
with open('D:\\dev-trash\\queries.txt') as f1:
	for row in f1:
		query = unicode(row.replace('\n','').decode('cp1251'))
		queries.append(query)
for query in queries:
	query = query.lower().encode('cp1251')
	print query