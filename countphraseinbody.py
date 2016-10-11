# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
data = requests.get('http://altpremium.ru/').text
data1 = re.sub('\<br\>',' ',data)
soup = BeautifulSoup(data1)
d = soup.body.get_text().split('\n')
d = [d1.lower() for d1 in d if d1 != '' and d1 != ' ']
for d1 in d:
    print d1
phrase = u'лицензии'
count = 0
for d1 in d:
    count += d1.count(phrase)