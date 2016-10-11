# -*- coding: utf-8 -*-
import math
from collections import Counter
import json
import requests

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def getURLs(query):
    urlsList = []
    url = 'http://seozoo.ru/api'
    payload = {
         "jsonrpc": "2.0",
         "method": "getYandexPosition",
         "params": {
                 "data": {
                     "lr": "213",
                     "query": query,
                     "zone": "ru"
                 },
                 "token": "UH7ForyW2o2QGIruyktzXbiivQ89EsEK197Ioccc"
         },
         "id":123
    }
    data = json.loads(requests.post(url,json.dumps(payload)).text)
    for dataItem in data['result']['results']:
         urlsList.append(dataItem['url'])
    return(urlsList)

counter_cosine_similarity(Counter(getURLs('оптимизация сайта')[0:24]), Counter(getURLs('продвижение сайта')[0:24]))