# -*- coding: utf-8 -*-
import requests

def parseLiData (data):
	liData = data.split(';\r\n')
	liData.remove(liData[-1])
	dataDict = {}
	for liDataItem in liData:
		liTuple = liDataItem.split(' = ')
		dataDict[liTuple[0]] = liTuple[1].replace("'","")
	return dataDict

def getLiveinternetMetrics (domain):
	url = 'http://counter.yadro.ru/values?site={0}'
	data = requests.get(url.format(domain)).text
	if 'LI_month_hit' in data:
		dataDict = parseLiData(data)
	else:
		dataDict = {'LI_day_hit': '0','LI_day_vis': '0','LI_month_hit': '0','LI_month_vis': '0','LI_online_hit': '0','LI_online_vis': '0','LI_site': domain,'LI_today_hit': '0','LI_today_vis': '0','LI_week_hit': '0','LI_week_vis': '0'}
	return dataDict


