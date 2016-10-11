#!/usr/bin/python
#coding=utf-8
from requests import Session
import pandas as pd
import cookielib,os,random,string,re
from datetime import datetime

URL_RET = 'https://direct.yandex.ru/registered/main.pl?cmd=showClients'
URL_PASSPORT = 'https://passport.yandex.ru/passport'

class DirectData(object):
	"""Get reports from Yandex Direct by Client-CampaignID tuples"""

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

	def _create_url_template(self,url):
		url = re.sub('main.*\.xls','main{0}.xls',re.sub('&cid=(\d)*.','&cid={0}&',re.sub('&ulogin=[a-z0-9-]*','&ulogin={1}',url)))
		return url

	def _get_report_content(self, url, client, campaignId):
		url = self._create_url_template(url)
		resp = self._session.get(url.format(campaignId,client))
		return resp.content

class FileWriter(object):
	"""Create folders and write xls-files with data"""
	def __init__(self, mainFolder):
		uniqueName = datetime.now().strftime("%y-%m-%d_%H-%M-%S_") + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
		if mainFolder[-1] != '\\':
			mainFolder += '\\'
		self._folderPath = mainFolder + uniqueName
		if not os.path.exists(self._folderPath):
			os.makedirs(self._folderPath)

	def _write_data_to_xls(self, data, campaignId):
		path = '{0}\\{1}.xls'.format(self._folderPath,campaignId)
		print path
		output = open(path, 'wb')
		output.write(data)
		output.close()

class PandasLayer(object):
	"""Read xls-files and concatenate in one file"""

	def __init__(self, folderPath):
		self._folderPath = folderPath
		self._dfs = []

	def _xls_to_df(self, client, campaignId):
		df = pd.read_excel('{0}\\{1}.xls'.format(self._folderPath,campaignId),skiprows=4,skip_footer=1)
		df[u'Кампания'] = campaignId
		df[u'Клиент'] = client
		self._dfs.append(df)

	def _concat_dfs_to_xls(self):
		uniqueName = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
		total_df = pd.concat(self._dfs)
		total_df.to_excel('{0}\\{1}.xlsx'.format(self._folderPath,uniqueName), sheet_name='Data')

class DataTuples(object):
	"""Create and process Client-CampaignID tuples"""

	def __init__(self):
		self._tuples = []

	def _from_tab(self, n_separated_string):
		n_separated_data = n_separated_string.split('\n')
		for item in n_separated_data:
			tab_separated_data = item.split('\t')
			if len(tab_separated_data) != 2:
				continue
			self._tuples.append(tuple(tab_separated_data))

	def _from_list(self, list_of_tuples):
		self._tuples = list_of_tuples

def ProcessTuples(tuples,path,login,password,url):
	dd = DirectData(login,password)
	fw = FileWriter(path)
	pl = PandasLayer(fw._folderPath)
	for client, campaignId in tuples:
		xls_content = dd._get_report_content(url,client,campaignId)
		fw._write_data_to_xls(xls_content,campaignId)
		pl._xls_to_df(client,campaignId)
	pl._concat_dfs_to_xls()

# pairs = [('avtozap4asti-ru-cubo','16093119'),('avtozap4asti-ru-cubo','16093105'),('avtozap4asti-ru-cubo','16093132'),('avtozap4asti-ru-cubo','16093125'),('avtozap4asti-ru-cubo','16009440'),('avtozap4asti-ru-cubo','16054179'),('avtozap4asti-ru-cubo','16009033'),('avtozap4asti-ru-cubo','16054170'),('c123btru-cubo','15733858'),('c123btru-cubo','15746190'),('nlv-ru-cubo','16040429'),('cubo-esis-ru','15362845'),('cubo-esis-ru','15364498'),('cubo-esis-ru','15229063'),('cubo-esis-ru','15233763'),('pravo-ved-cubo','15904805'),('pravo-ved-cubo','15950729')]
# path = 'D:\\direct_data\\'
# dd = DirectData('Alexgrtula','DhYwOHrW')
# fw = FileWriter(path)
# pdf = PandasDataFrame(fw._folderPath)
# url = 'https://direct.yandex.ru/registered/04.01-11.01_main16009033.xls?filter_banner=&isStat=1&with_avg_position=1&m2=01&ulogin=avtozap4asti-ru-cubo&cmd=showCampStat&filter_gender=&stat_type=custom&filter_age=&d2=11&y1=16&filter_phrase=&filter_geo=&online_stat=1&filter_page_target=&goals=0&cid=16009033&filter_retargeting=&filter_page=&filter_tag=&offline_stat=0&with_auto_added_phrases=1&d1=04&filter_position=&group=day&group_by=tag%2C%20adgroup%2C%20banner%2C%20page%2C%20phrase%2C%20retargeting%2C%20geo%2C%20position%2C%20image%2C%20device_type%2C%20gender%2C%20age%2C%20date&y2=16&save_nds=1&filter_device_type=&filter_image=&stat_periods=2015-12-09%3A2016-01-03%2C2015-12-01%3A2016-01-11%2C2016-01-01%3A2016-01-11&with_nds=1&m1=01&filter_adgroup=&currency_archive=&onpage=100&xls=1'
# for CLIENT,CID in pairs:
#     print 'Process: campaign {0}'.format(CID)
#     content = dd._get_report_content(url,CLIENT,CID)
#     fw._write_data_to_xls(content,CID)
#     pdf._xls_to_df(CLIENT,CID)
# pdf._concat_dfs_to_xls()


data = '''avtozap4asti-ru-cubo	16093119
avtozap4asti-ru-cubo	16093105
avtozap4asti-ru-cubo	16093132
avtozap4asti-ru-cubo	16093125
avtozap4asti-ru-cubo	16009440
avtozap4asti-ru-cubo	16054179
avtozap4asti-ru-cubo	16009033
avtozap4asti-ru-cubo	16054170
c123btru-cubo	15733858
c123btru-cubo	15746190
nlv-ru-cubo	16040429
cubo-esis-ru	15362845
cubo-esis-ru	15364498
cubo-esis-ru	15229063
cubo-esis-ru	15233763
pravo-ved-cubo	15904805
pravo-ved-cubo	15950729
'''
dt = DataTuples()
dt._from_tab(data)
path = 'D:\\direct_data\\'
login = 'Alexgrtula'
password = 'DhYwOHrW'
url = 'https://direct.yandex.ru/registered/04.01-11.01_main16009033.xls?filter_banner=&isStat=1&with_avg_position=1&m2=01&ulogin=avtozap4asti-ru-cubo&cmd=showCampStat&filter_gender=&stat_type=custom&filter_age=&d2=11&y1=16&filter_phrase=&filter_geo=&online_stat=1&filter_page_target=&goals=0&cid=16009033&filter_retargeting=&filter_page=&filter_tag=&offline_stat=0&with_auto_added_phrases=1&d1=04&filter_position=&group=day&group_by=tag%2C%20adgroup%2C%20banner%2C%20page%2C%20phrase%2C%20retargeting%2C%20geo%2C%20position%2C%20image%2C%20device_type%2C%20gender%2C%20age%2C%20date&y2=16&save_nds=1&filter_device_type=&filter_image=&stat_periods=2015-12-09%3A2016-01-03%2C2015-12-01%3A2016-01-11%2C2016-01-01%3A2016-01-11&with_nds=1&m1=01&filter_adgroup=&currency_archive=&onpage=100&xls=1'
ProcessTuples(dt._tuples,path,login,password,url)


# to-do:
# Прикрутить логгер
# Сделать парсер пар: из xlsx или xls
# Прикрутить автоподтягивалку клиент-ид, подтягивать все кампании по клиенту - нужно привязаться к базе на 7.8