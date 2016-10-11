# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

def getDomainTCY(domain):
    dataDict = {}
    dataDict['domain'] = domain
    r = requests.get('http://bar-navig.yandex.ru/u?ver=2&url={0}&show=1'.format(domain))
    print '1. Сделали реквест'
    soup = BeautifulSoup(r.text, 'lxml')
    print '2. Распарисили xml'
    dataDict['tcy'] = soup.tcy['value']
    print '3. Получили тиц'
    dataDict['rang'] = soup.tcy['rang']
    print '4. Получили ранг'
    if soup.find('topic'):
        dataDict['topic'] = soup.topics.topic['title'].replace(u'Тема: ','')
        textinfo = soup.textinfo.get_text()
        for textInfoItem in textinfo.split('\n'):
            if u'Регион' in textInfoItem:
                dataDict['region'] = textInfoItem.replace(u'Регион: ','')
            if u'Источник' in textInfoItem:
                dataDict['source'] = textInfoItem.replace(u'Источник: ','')
            if u'Сектор' in textInfoItem:
                dataDict['sector'] = textInfoItem.replace(u'Сектор: ','')
        print '5. Получили тематику'
    return dataDict

def getTCYbyDomains(domains):
    data = []
    domainsCount = len(domains)
    i = 1
    for domain in domains:
        print 'Делаю домен {0} из {1}: {2}'.format(i,domainsCount,domain)
        domainData = getDomainTCY(domain)
        if 'domain' in domainData.keys():
            data.append(domainData)
            print 'Добавили данные'
        i += 1
    return data

def createCSVFromData(data,filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath,encoding='utf-8')