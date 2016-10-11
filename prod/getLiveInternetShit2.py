# -*- coding: utf-8 -*-
import logging
import requests
from itertools import islice
from datetime import datetime
import json

logdate = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG, filename = u'D:\\liGetterLog2_{0}.log'.format(logdate))

# f = "D:\\domains\\ru_domains"
# count = 500
def getDomainsFromTextFile(f,count,offset): 
    with open(f) as myfile:
        head = list(islice(myfile, offset-1, offset+count-1))
    domains = []
    for row in head:
        splittedRow = row.split('\t')
        splittedRow = [s.replace('\n','').lower() for s in splittedRow]
        d = {}
        d['domain'] = splittedRow[0]
        d['registrar'] = splittedRow[1]
        d['created'] = splittedRow[2]
        d['paid-till'] = splittedRow[3]
        d['free-date'] = splittedRow[4]
        domains.append(d)
    return domains

# domain = 'damageinfo.ru'
# searchEngine = 'yandex'
# date = '2015-10-31'
# page = 1
def getLiveinternetResponse(domain,searchEngine,date,page):
    try:
        url = 'http://www.liveinternet.ru/stat/{0}/{1}.csv?date={2}&period=month&per_page=100&page={3}'.format(domain,searchEngine,date,page)
        proxies = {'http': 'http://94.77.88.2:3001'}
        data = requests.get(url, proxies=proxies).text.split('\n')
        logging.info(u'В результатах {0} строк'.format(len(data)))
        return data
    except:
        logging.error(u'Requests error')
        pass

# data = getLiveinternetResponse(domain,searchEngine,date,page)
def getQueriesFromLiveInternetCSV(data):
    queries = []
    columnsNames = data[0].split(';')
    logging.info(u'Собираем данные из LI. Получили {0} запросов'.format(len(data[1:])))
    for row in data[1:]:
        splittedRow = row.split(';')
        if len(splittedRow) < 3:
            continue
        query = splittedRow[0][1:-1]
        for i in xrange(0,2):
            period = columnsNames[i+1][1:-1]
            value = splittedRow[i+1]
            queries.append({'query':query,'period':period,'value':value})
    return queries


f = "D:\\domains\\ru_domains"
count = 1000
offset = 300
domains = getDomainsFromTextFile(f,count,offset)
domainsCount = len(domains)
allData = []
counter = 1
for item in domains:
    domainQueries = []
    domain = item['domain']
    logging.debug(u'Получаем данные для {0} домена из {1}: {2}'.format(counter,domainsCount,domain))
    isNotData = False
    counter += 1
    searchEngines = ['yandex']
    for searchEngine in searchEngines:
        if isNotData:
            break
        logging.debug(u'Выбираем данные по поисковой системе {0}'.format(searchEngine))
        dates = ['2015-11-30','2015-10-31','2015-09-30','2015-08-31']
        for date in dates:
            if isNotData:
                break
            logging.debug(u'Выбираем данные за {0}'.format(date))
            previousData = []
            for pageCounter in xrange(1,11):
                logging.debug(u'Делаем страницу {0}'.format(pageCounter))
                data = getLiveinternetResponse(domain,searchEngine,date,pageCounter)
                rowsCount = len(data)
                if data == previousData or rowsCount < 4:
                    if unicode('"статистика сайта";"обновлено {date} в {time}"'.decode('utf-8')) in data:
                        logging.warning(u'Статистика LiveInternet отсутствует')
                        isNotData = True
                    else:
                        logging.warning(u'Страница не содержит информации')
                    break
                logging.info(u'Данные есть: {0}'.format(rowsCount))
                domainQueries += getQueriesFromLiveInternetCSV(data)
                if rowsCount == 103:
                    logging.info(u'Есть следующая страница')
                    previousData = data
                else:
                    logging.info(u'Страница последняя')
                    break
    for domainQuery in domainQueries:
        domainQuery['domain'] = domain
    allData += domainQueries
uniqueQueries = list(set([q['query'] for q in allData]))
logging.debug(u'Всего запросов: {0}'.format(len(uniqueQueries)))
with open('D:\\queriesData.json','w+') as f1:
    print >>f1,json.dumps(allData)
with open('D:\\uniqueQueries.json','w+') as f1:
    print >>f1,json.dumps(uniqueQueries)