# -*- coding: utf-8 -*-
import json
import io
import uuid
from urlparse import urlparse
import tldextract
import re

f1 = io.open('D:\\rtb\\clear.txt','r+')
f2 = open('D:\\rtb\\output.txt','w+')
data = json.load(f1, encoding='utf-8')
i = 0
for item in data:
	userID = unicode(uuid.uuid1())
	i += 1
	j = 0
	domains = []
	for g in item['data']:
		j += 1
		if 'page' in g:
			page = g['page'].replace('http://ads.betweendigital.com/adi?ref=','')
			deleted = ['adriver.ru','adwolf.ru']
			matching = False
			for deleted1 in deleted:
				if deleted1 in page:
					matching = True
			uri = urlparse(page)
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)
			if not matching:
				extracted = tldextract.extract(domain)
				domainwosub = "{}.{}".format(extracted.domain, extracted.suffix)
				domainwsub = "{}.{}.{}".format(extracted.subdomain, extracted.domain, extracted.suffix)
				if domainwsub[0] == ".":
					domainwsub = domainwsub[1:]
				date = g['date'].split('T')
				time = date[1].replace('Z','')
				time = re.sub('\.(.*)','',time)
				print >>f2, u'{}\t{}\t{}\t{}\t{}\t{}'.format(userID,date[0],time,domain,domainwosub,domainwsub).encode('utf-8')
	print '{0} \t {1}'.format(userID, j)
print i
print g