# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
def getLiveinternetQueries (site):
	r = requests.get ('http://www.liveinternet.ru/stat/{0}/yandex.html?period=month&per_page=100'.format(site))
	soup = BeautifulSoup(r.text, 'html.parser')
	if ('Для доступа к этой странице необходимо ввести пароль'.decode('utf-8') in soup.get_text()) or ('Ошибка: сайт с таким адресом не зарегистрирован'.decode('utf-8') in soup.get_text()):
		return 0
	else:
		queries = []
		for label in soup.find_all('label'):
			queries.append(label.get_text())
		return queries

sites1 = ['lamoda.ru','booking.com','su155.ru','fursk.ru','smclinic.ru','tripadvisor.ru','ozon.travel','alefmex.ru','urbangroup.ru','homeme.ru','morton.ru','delivery-club.ru','onclinic.ru','kvadroom.ru','dubna-center.ru','city-mobil.ru','pizzasushiwok.ru','svyaznoy.ru','price.ru','ndv.ru','doct.ru','pik.ru','profi.ru','westwing.ru','gruzovichkof.ru','dorian.ru','anywayanyday.com','novostroy-m.ru','loranmebel.ru','abada.ru','kv-istra.ru','askona.ru','tcsbank.ru','hoff.ru','alpari.ru','sberbank.ru','citilink.ru','tk-konstruktor.ru','mvideo.ru','fxclub.org','etaloncity.ru','kupivip.ru','alibra.ru','ozon.ru','flor2u.ru','remont-f.ru','akmmos.ru','eldorado.ru','ticketland.ru','specialist.ru','onetwotrip.com','englishfirst.ru','ulmart.ru','marshak.ru','mebelvia.ru','gazelkin.ru','tsarvkusa.ru','mosmexa.ru','hotels.com','ecopotolki.com','incom.ru','strd.ru','best-novostroy.ru','izumrudnie-holmi.ru','enjoyflowers.ru','1331.ru','medsi.ru','aeroflot.ru','okonremont.ru','momza.ru','tvoymeh.ru','holodilnik.ru','stilkuhni.ru','gettable.ru','fabrikaokon.ru','xn----7sba5akcbwhbc0an.xn--p1ai','tinkoffinsurance.ru','wix.com','vamsvet.ru','gwd.ru','bmw-avilon.ru','okna-21-veka.ru','quadro-design.ru','wikimart.ru','ipizza.ru','elenafurs.ru','mos-olimp.ru','vianor-tyres.ru','banki.ru','avto-kapital.ru','gorkigroup.ru','oknagorizont.ru','renault.ru','auto.ru','zoomby.ru','mercedes-panavto.ru','dianafurs.ru','interlaz.ru','ronikon.ru','mgts.ru','isolux.ru','svyaznoy.travel','narkopro.ru','blizko.ru','cnn.msk.ru','sminex.com','nissan.ru','moon-trade.ru','aviasales.ru','genvik.ru','sr-okna.com','2878888.ru','stolplit.ru','megapolistaxi.ru','digitalserv.ru','mir-realty.ru','portaprima.ru','timberlandzz.ru','estee-design.ru','quelle.ru','ostrovok.ru','move.su','cvetydushi.ru','life-capital.ru','mediccity.ru','krost-realty.ru','porsche-moscow.ru','rehabclinic.ru','glawmebel.ru','pleer.ru','otrada.estate','biglion.ru','unikma.ru','rencredit.ru','tutu.ru','mc-euromed.ru','enter.ru','taxi.msk.ru','stream-auto.ru','vipegrul.ru','svservis.ru','timberland.net.ru','spim.ru','mercedes-mbr.ru','terem-pro.ru','masterdom.ru','stolica77.ru','remontokon24.ru','okna-remont.ru','zao-lombard.ru','parkrublevo.ru','good-mebel.com','yit-dom.ru','lukinovarino.ru','sa.ru','top-shop.ru','ormatek.com','sauna.ru','zdorovie-narcology.ru','ford-avilon.ru']
sites2 = ['damageinfo.ru']
sitesCount = len(sites1)
f2 = open('D:\\dev-trash\\queriesfromliru.txt','w+')
i = 1
for site in sites1:
	print '{0}: {1} in {2}'.format(site,i,sitesCount)
	a = lgetLiveinternetQueries(site)
	if a != 0:
		print 'Yes. Its OK'
		for query in a:
			print >>f2, '{0}\t{1}'.format(site.encode('utf-8'),query.encode('utf-8'))
	else:
		print 'Cant get you out off my queries'
	i += 1