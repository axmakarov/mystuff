def getDomainByCampaignID (campaign):
	d = {}
	print 'Получаем данные для кампании {0}'.format(campaign)
	directPayload = {
	"method": "GetBanners", "token": "cc8fb959428d401a98ab953b75693f2e","param": {"CampaignIDS": [campaign]}}
	r = requests.post('https://api.direct.yandex.ru/live/v4/json/',json.dumps(directPayload))
	print 'Получили реквест:'
	data = json.loads(r.text)
	if 'data' in data.keys():
		print 'В ответе {0} объявлений'.format(len(data['data']))
		uri = urlparse(data['data'][0]['Href'])
		d[str(campaign)] = uri.netloc
		print 'Получили домен: {0}'.format(uri.netloc.encode('utf-8'))
	else:
		print 'Ересь в ответе'
		print data
		d[str(campaign)] = 'error'
	return d



arr = []
i = 1
count = len(campaigns)
for campaign in campaigns:
	print '{0} из {1}:'.format(i,count)
	arr.append (getDomainByCampaignID(campaign))
	i += 1