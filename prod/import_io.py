# -*- coding: utf-8 -*-
API_KEY = 'fe02c38216d14d62a43c0ca3bf9b9fcd9f5d63886a1d3e7afd54433e47d8402c0fcc9c50a7714af7034ed86dfdf88428a21f0cfc7a0c3c22c7587ae528a986bd81266d8893183098f24ff06f95b4df97'

def getDataByUrl(url,js):
# Получает ответ от Import.io
# url = адрес страницы для сбора контента
# js = обрабатывать ли Javascript (boolean) 
    url = 'https://api.import.io/store/connector/_magic?url={0}&format=json&js={1}&_apikey={2}'.format(url,str(js),API_KEY)
    return json.loads(requests.get(url).text)

def getTables(data):
# Получает список таблиц данных из ответа Import.io
# data = ответ, полученный функцией getDataByUrl
    return data['tables']

def getResultsFromTable(table):
# Получает все результаты из отдельно взятой таблицы данных
# table = таблица данных
    results = []
    if isLinkInTableOutputProperties(table):
        for result in table['results']:
            results.append(result)
    return results

def getNeedItemsFromOutputProperties(outputProperties):
    items = []
    for op in outputProperties:
        if op['type'] == 'URL':
            items.append(op['name'])
    return items

def isLinkInTableOutputProperties(table):
    isLink = False
    outputProperties = table['outputProperties']
    for item in outputProperties:
        if item['type'] == 'URL':
            isLink = True
    return isLink

def getAllResultsFromPage(tables):
# Получает результаты из всего списка таблиц (Результаты только, содержащие ссылки)
    datas = []
    for table in tables:
        needItems = getNeedItemsFromOutputProperties(table['outputProperties'])
        results = getResultsFromTable(table)
        if len(results) > 0:
            for result in results:
                for k in result.keys():
                    if k in needItems:
                        result['link_keys'] = needItems
                        datas.append(result)
    return datas

# Как использовать
url = 'http://www.da-baby.ru/catalog/kolyaski/'
data = getDataByUrl(url,False)
parsedResults = getAllResultsFromPage(getTables(data))