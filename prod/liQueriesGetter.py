# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
def getLiveinternetQueries (site):
	r = requests.get ('http://www.liveinternet.ru/stat/{0}/yandex.html?period=month&per_page=100'.format(site))
	soup = BeautifulSoup(r.text, 'html.parser')
	if ('Для доступа к этой странице необходимо ввести пароль'.decode('utf-8') in soup.get_text()) or ('Ошибка: сайт с таким адресом не зарегистрирован'.decode('utf-8') in soup.get_text()):
		return 0
	else:
		queries = []
		for label in soup.find_all('label'):
			queries.append(label.get_text())
		return queries

# d = []
# count = len(sites)
# i = 1
# for site in sites:
#     print 'Делаю сайт {0} из {1}: {2}'.format(i,count,site)
#     k = getLiveinternetQueries(site)
#     if k != 0:
#         print 'Получили данные: {0}'.format(len(k))
#         for query in k:
#             d1 = {}
#             d1['domain'] = site
#             d1['query'] = query
#             d.append(d1)
#     i += 1