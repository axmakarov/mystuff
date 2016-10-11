import json
import requests
from bs4 import BeautifulSoup
import pymorphy2
import math
from collections import Counter

morph = pymorphy2.MorphAnalyzer()

def getXMLData(query,lr):
    query = query.encode('utf-8')
    URL = 'http://seozoo.ru/xmlsearch?user=aleksey.makarov@ingate.ru&key=UH7ForyW2o2QGIruyktzXbiivQ89EsEK197Ioccc&query={0}&lr={1}&l10n=ru&sortby=rlv&filter=moderate&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D100.docs-in-group%3D1'.format(query,lr)
    print URL
    return requests.get(URL).content

def parseXMLData(data):
    Soup = BeautifulSoup(data)
    results = Soup.find_all('results')[0]
    docs = results.find_all('doc')
    return docs

def GetNormalForm(word):
    return morph.parse(word)[0].normal_form

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def CreateCounter(tag):
    counter = Counter()
    text = CleanStopWords(ClearQuery(tag.get_text().replace('-',' ')))
    text = ' '.join([GetNormalForm(word) for word in text.split(' ')])
    for word in text.split(' '):
        counter[word] += 1
    return counter

def GetTextCounters(XMLData):
    titleCounter = Counter()
    descCounter = Counter()
    domainCounter = Counter()
    urlCounter = Counter()
    for item in XMLData:
        for tag in item.find_all('title'):
            titleCounter += CreateCounter(tag)
        for tag in item.find_all('passage'):
            descCounter += CreateCounter(tag)
        for tag in item.find_all('domain'):
            domainCounter[tag.get_text()] += 1
        for tag in item.find_all('url'):
            urlCounter[tag.get_text()] += 1
    return titleCounter,descCounter,domainCounter,urlCounter

def calculateSimilarityMetrics(mainPhrase,childPhrase,lr):
    mainPhraseData = getXMLData(mainPhrase,lr)
    childPhraseData = getXMLData(childPhrase,lr)
    mainPhraseCounters = GetTextCounters(parseXMLData(mainPhraseData))
    childPhraseCounters = GetTextCounters(parseXMLData(childPhraseData))
    titleSimilarity = counter_cosine_similarity(mainPhraseCounters[0],childPhraseCounters[0])
    descSimilarity = counter_cosine_similarity(mainPhraseCounters[1],childPhraseCounters[1])
    domainSimilarity = counter_cosine_similarity(mainPhraseCounters[2],childPhraseCounters[2])
    urlSimilarity = counter_cosine_similarity(mainPhraseCounters[3],childPhraseCounters[3])
    return titleSimilarity,descSimilarity,domainSimilarity,urlSimilarity

# calculateSimilarityMetrics(u'купить телефон sony',u'купить телефон sony xperia',15)

