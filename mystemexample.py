# -*- coding: utf-8 -*-
import json
from pymystem3 import Mystem
import re

def lemmatize(text):
	m = Mystem()
	lemmas = m.lemmatize(text)
	return (''.join(lemmas))

# print lemmatize('мама мыла раму').decode('utf-8')
text = unicode("124#21413 fdsfs*fsdfs авыаы№авы".decode('utf-8'))
line = re.sub(r'[^a-zA-Z0-9а-яА-Я\s.-]',' ',text,flags=re.UNICODE)
print >>open('D:\\regoutput.txt','w+'), line.encode('utf-8')