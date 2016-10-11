# -*- coding: utf-8 -*-
import random
import json

# Создаем случайную статистику коэффициентов затухания для тематик
def createRandomThemesAttenuationConstant(filename):
	themesFile = open (filename, 'w+')

	themesAttenuationConstant = dict([('theme1',random.randint(11,99)/10.0),('theme2',random.randint(11,99)/10.0),('theme3',random.randint(11,99)/10.0),('theme4',random.randint(11,99)/10.0)])
	print >>themesFile, json.dumps(themesAttenuationConstant)
	return themesAttenuationConstant

# Создаем случайную статистику доменов
def createRandomDomains(filename):
	domainFile = open (filename, 'w+')

	domains = []
	domainsCount = random.randint (1,10) # Создаем случайное количество доменов
	counter = 1
	while counter <= domainsCount:
		domainID = counter
		themes = dict([('theme1',random.random()),('theme2',random.random()),('theme3',random.random()),('theme4',random.random())]) # Создаем словарь из 4 тематик со случайными весами
		domain = dict([('domainID',domainID),('themes',themes)])
		domains.append (domain)
		counter += 1
	print >>domainFile, json.dumps(domains)
	return domains

# Создаем случайный визит
def createRandomVisit(domains):
	visit = random.choice(domains)
	return visit

statistics = open ('D:\\rtbstat\\statistics.json','w+')
statisticstxt = open('D:\\rtbstat\\statistics.txt','w+')
agrstattxt = open ('D:\\rtbstat\\argstat.txt','w+')

themesAttenuationConstant = createRandomThemesAttenuationConstant('D:\\rtbstat\\themesAttenuationConstant.json')
domains = createRandomDomains('D:\\rtbstat\\domains.json')

agrStat = dict([('theme1',0.0),('theme2',0.0),('theme3',0.0),('theme4',0.0)])

domainsCount = len(domains)
days = []
daysCount = random.randint (15,30)
dayCounter = 1
totalCounter = 1
while dayCounter <= daysCount:
	for key, value in agrStat.iteritems():
		agrStat[key] = agrStat[key]/themesAttenuationConstant[key]
	visitsCount = random.randint(1,domainsCount*3)
	visitCounter = 1
	visits = []
	while visitCounter <= visitsCount:
		visit = dict([('visitCount',totalCounter),('domain',createRandomVisit(domains))])
		for k,v in visit['domain']['themes'].iteritems():
			agrStat[k] = agrStat[k] + v
		visits.append(visit)
		print >>statisticstxt, '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(dayCounter,visitCounter,totalCounter,visit['domain']['domainID'],visit['domain']['themes']['theme1'],visit['domain']['themes']['theme2'],visit['domain']['themes']['theme3'],visit['domain']['themes']['theme4'])
		visitCounter += 1
		totalCounter += 1
	print >>agrstattxt, '{}\t{}\t{}\t{}\t{}'.format(dayCounter,agrStat['theme1'],agrStat['theme2'],agrStat['theme3'],agrStat['theme4'])
	day = dict([('dayCount',dayCounter),('visits',visits)])
	days.append(day)
	dayCounter += 1

print >>statistics, json.dumps(days)



