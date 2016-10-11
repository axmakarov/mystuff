from grab import Grab
from bs4 import BeautifulSoup
import pandas as pd
g = Grab()
g.go('https://passport.yandex.ru/auth')
g.doc.set_input('login', 'RookeeXML')
g.doc.set_input('passwd', 'pass-RookeeXML')
g.doc.submit()
g.go('https://direct.yandex.ru/registered/main.pl?cmd=showCompetitors&phrase={0}&geo={1}&size=100'.format('коляски stokke','213'))
soup = BeautifulSoup(g.doc.body,'lxml')
data = []
for tag in soup.find_all(attrs={"class": "b-competitors-banners-list__banner-container"}):
    title = tag.find(attrs={"class": "b-link b-banner-preview__title"})
    if title.get('href'):
        href = title['href']
    else:
        href = ''
    title = title.get_text()
    public_identity = json.loads(tag.find(attrs={"data-bem": re.compile("b-banner-preview")})['data-bem'])['b-banner-preview']['publicIdentity']
    body = tag.find(attrs={"class": "b-banner-preview__body"}).get_text()
    domain = tag.find(attrs={"class": "b-banner-preview__domain"})
    if domain:
        domain = domain.get_text()
    vcard = tag.find(attrs={"class": "b-banner-preview__vcard"})
    if vcard:
        vcard = json.loads(vcard['data-bem'])['b-modal-popup-opener']['url']
    regions = tag.find(attrs={"class": "b-group-regions__names-popup i-bem"})
    if regions:
        regions = json.loads(regions['data-bem'])['b-group-regions__names-popup']['names']
    else:
        regions = tag.find(attrs={"class": "b-group-regions__names"}).get_text()
    dict1 = {'title': title, 'body': body, 'domain': domain, 'regions': regions, 'href': href, 'vcard': vcard, 'public_identity': public_identity}
    data.append(dict1)
df = pd.DataFrame(data)