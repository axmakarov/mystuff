import requests
from bs4 import BeautifulSoup

def getLinkpadData(domain):
    url = 'http://xml.linkpad.ru/?url=http://{0}'
    data = requests.get(url.format(domain)).text
    soup = BeautifulSoup(data,'lxml')
    dataDict = {}
    dataDict['host'] = soup.host.get_text()
    dataDict['index'] = int(soup.find('index').get_text())
    for i in xrange(0,4):
        dataDict['hin_l'+str(i+1)] = soup.hin['l'+str(i+1)]
        dataDict['din_l'+str(i+1)] = soup.din['l'+str(i+1)]
        dataDict['hout_l'+str(i+1)] = soup.hout['l'+str(i+1)]
    dataDict['hin'] = int(soup.hin.get_text())
    dataDict['din'] = int(soup.din.get_text())
    dataDict['hout'] = int(soup.hout.get_text())
    dataDict['dout'] = int(soup.dout.get_text())
    dataDict['anchors'] = int(soup.anchors.get_text())
    dataDict['igood'] = soup.igood.get_text()
    return dataDict