from requests import Session
import pandas as pd
import cookielib,os,random,string,re
from datetime import datetime

class DirectXlsData(object):

	def __init__(self, login, password):
		self._login = login
		self._password = password
		self._session = Session()
		self._session.cookies = cookielib.CookieJar()
		self._auth()

	def _auth(self):
		params = {'mode': 'auth',
				  'retpath': URL_RET}
		data = {'login': self._login,
				'passwd': self._password,
				'retpath': URL_RET}
		response = self._session.post(URL_PASSPORT,
			params=params,
			data=data,
			allow_redirects=True)

	def _getXlsData(self, url):
		return session.get(url).content

def getCampaignIdAndLoginFromUrl (url):
	campaignId = re.findall('cid=(.+?)&',url)[0]
	login = re.findall('ulogin=(.+?)&',url)[0]
	return campaignId,login

def createFolder (mainFolder,login):
	uniqueName = datetime.now().strftime("%y-%m-%d_%H-%M-%S_") + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
	if mainFolder[-1] != '\\':
		mainFolder += '\\'
	folderPath = mainFolder + login
	if not os.path.exists(folderPath):
			os.makedirs(folderPath)
	return folderPath

def writeDataToXls (data,folderPath,campaignId):
	path = '{0}\\{1}.xls'.format(folderPath,campaignId)
	print path
	output = open(path, 'wb')
	output.write(data)
	output.close()

# urls = ['https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=14248951&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=16455762&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=16456278&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=16470748&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=14258619&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=16455287&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=16456003&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=16456125&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=okna-okoshkino-cubo&cid=16470199&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=baltmed-ru-cubo&cid=16251639&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=baltmed-ru-cubo&cid=16350742&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=schenyachiy-patrul-com-cubo&cid=16436018&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=schenyachiy-patrul-com-cubo&cid=16435957&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&cid=15539555&ulogin=optikdeal-ru-cubo&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=optikdeal-ru-cubo&cid=15537079&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&ulogin=optikdeal-ru-cubo&cid=15537368&skip_arch=on&xls_format=xls','https://direct.yandex.ru/registered/main.pl?cmd=exportCampXLS&cid=15534590&ulogin=optikdeal-ru-cubo&skip_arch=on&xls_format=xls']
# login = 'Alexgrtula'
# password = 'DhYwOHrW'
# dxd = DirectXlsData(login,password)
# for url in urls:
#     xls_content = dxd._getXlsData(url)
#     campLogin = getCampaignIdAndLoginFromUrl(url)[1]
#     campaignId = getCampaignIdAndLoginFromUrl(url)[0]
#     folderPath = createFolder('D:\\direct_data\\',campLogin)
#     writeDataToXls(xls_content,folderPath,campaignId)