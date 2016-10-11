# -*- coding: utf-8 -*-
import requests
import json

def getVisibility(lr,domain,date):
    data = []
    url = 'http://api.megaindex.ru/?method=siteAnalyze&login=ax.makarov@yandex.ru&password=wae8Useisa&lr={0}&url={1}&date={2}'.format(str(lr),domain,date)
    reqData = json.loads(requests.get(url).text)
    for dataItem in reqData['data'][1:]:
        dataDict = {}
        dataDict['domain'] = domain
        dataDict['query'] = dataItem[0]
        dataDict['yandex'] = dataItem[1]
        dataDict['na'] = dataItem[2]
        dataDict['google'] = dataItem[3]
        dataDict['visibility'] = dataItem[4]
        dataDict['impressions'] = dataItem[5]
        dataDict['wordstat1'] = dataItem[6]
        dataDict['wordstat2'] = dataItem[7]
        dataDict['livisits'] = dataItem[8]
        dataDict['effimp'] = dataItem[9]
        dataDict['price'] = dataItem[10]
        dataDict['effprice'] = dataItem[11]
        dataDict['effimpprice'] = dataItem[12]
        dataDict['comprice'] = dataItem[13]
        dataDict['direct'] = dataItem[14]
        dataDict['adwords'] = dataItem[15]
        dataDict['wordid'] = dataItem[16]
        data.append(dataDict)
    return data

def getBacklinks(domain):
	url = 'http://api.megaindex.ru/?method=get_backlinks&output=json&login=ax.makarov@yandex.ru&password=wae8Useisa&url={0}'.format(domain)
	data = json.loads(requests.get(url).text)
	return data