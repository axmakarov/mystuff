# -*- coding: utf-8 -*-
import tldextract
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

def has_class_b(tag):
    return tag.has_attr('class') and tag['class'] == ['b-whois-info__info']


def getDomainCreationDate(domain):
    availableSuffixes = ['ru','su','XN--P1AI','xn--p1ai','spb.ru','msk.ru','pl','net','com','ua','se','no','it','md','info','org','moscow','travel','tv','cc','pro','in','bz','ws','kz']
    extracted = tldextract.extract(domain)
    mainDomain = "{}.{}".format(extracted.domain, extracted.suffix)
    suffix = extracted.suffix
    if not suffix in availableSuffixes:
        createddate = '0000.00.00'
    else:
        r = requests.get('https://www.nic.ru/whois/?query={0}'.format(mainDomain))
        soup = BeautifulSoup(r.text, 'lxml')
        if len(soup.find_all(has_class_b)) > 0:
            data = soup.find_all(has_class_b)[0].get_text()
            if suffix in ['ru','su','XN--P1AI','xn--p1ai','spb.ru','msk.ru','pl']:
                createddate = re.findall(u'created:.*\n',data)[0]
                createddate = re.findall('\d{4}\.\d{2}\.\d{2}$',createddate)[0]
                createdt = datetime.strptime(createddate, "%Y.%m.%d")
            elif suffix in ['net','com']:
                createddate = re.findall(u'Creation Date:.*\n',data)[0]
                createddate = re.findall('\d{1,2}.*\d{4}$',createddate)[0]
                createdt = datetime.strptime(createddate, "%d-%b-%Y")
            elif suffix in ['ua','se','no','it','md']:
                createddate = re.findall(u'created:.*\n',data,flags=re.IGNORECASE)[0]
                createddate = re.findall(u'\d{4}-\d{2}-\d{2}',createddate)[0].replace(' ','')
                createdt = datetime.strptime(createddate, "%Y-%m-%d")
            elif suffix in ['info','org','moscow','travel','tv','cc']:
                createddate = re.findall(u'Creation Date:.*\n',data)[0]
                createddate = re.findall('\d{4}-\d{2}-\d{2}T',createddate)[0].replace('T','')
                createdt = datetime.strptime(createddate, "%Y-%m-%d")
            elif suffix in ['pro','in','bz']:
                createddate = re.findall(u'Created On:.*\n',data)[0]
                createddate = re.findall('\d{2}-.*-\d{4}\s',createddate)[0].replace(' ','')
                createdt = datetime.strptime(createddate, "%d-%b-%Y")
            elif suffix in ['ws']:
                createddate = re.findall(u'Creation Date:.*\n',data)[0]
                createddate = re.findall('\d{4}-.*-\d{2}$',createddate)[0].replace(' ','')
                createdt = datetime.strptime(createddate, "%Y-%m-%d")
            elif suffix in ['kz']:
                createddate = re.findall(u'Domain created:.*\n',data)[0]
                createddate = re.findall('\d{4}-\d{2}-\d{2}',createddate)[0].replace(' ','')
                createdt = datetime.strptime(createddate, "%Y-%m-%d")
            createddate = createdt.strftime("%d.%m.%Y")
        else:
            createddate = '0000.00.00'
    return createddate