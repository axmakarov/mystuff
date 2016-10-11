# -*- coding: utf-8 -*-
import lxml.html
from lxml.cssselect import CSSSelector

url = 'http://www.onkodoktor.ru'
t = lxml.html.parse(url)
print t.find(".//title").text
x = t.tostring ()
