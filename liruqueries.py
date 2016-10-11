# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
sites = ['damageinfo.ru']
siteInfo = []
f1 = open('D:\\dev-trash\\liveinternetqueries.txt','w+')
for site in sites:
	r = requests.get('http://www.liveinternet.ru/stat/{}/yandex.html?period=month&per_page=100'.format(site))
	soup = BeautifulSoup(r.text, 'html.parser')
	queries = []
	for label in soup.find_all('label'):
		queries.append(label.get_text())
		print >>f1, '{0}\t{1}'.format(site,label.get_text().encode('utf-8'))
	siteInfo.append(dict([('site',site),('queries',queries)]))
