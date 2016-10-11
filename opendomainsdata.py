# -*- coding: utf-8 -*-
import json
import io

f1 = io.open('D:\\rtb\\domains4.txt','r+',encoding='utf-8')
f2 = open('D:\\rtb\\outputdomains.txt','w+')
data = json.load(f1)
i = 0
z = 0
for d,v in data.iteritems():
	# k хранит в себе название домена
	for key,value in v.iteritems():
		print >>f2, '{}\t{}\t{}'.format(d, key.encode('utf-8'), value)
	i += 1
print i