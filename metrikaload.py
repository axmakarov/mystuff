#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
url = 'https://beta.api-metrika.yandex.ru/stat/v1/data?ids=29392580&dimensions=ym:s:UTMContent,ym:s:UTMMedium&metrics=ym:s:visits,ym:s:bounceRate&limit=10000&offset=1&oauth_token=a5bce64b0f9b4caeacb69465ef7f89d7&date1=2015-04-11&date2=2015-04-19'
r = requests.get(url)
f1 = open('D:\\dev-trash\\json-test.json', 'w+')
print >>f1, r.text

