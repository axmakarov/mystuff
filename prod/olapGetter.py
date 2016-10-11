import json
import requests
from datetime import timedelta, datetime
from operator import itemgetter

def createOlapPayload(source,metrics,dimensions,startDate,endDate,filters):
	data = {}
	data['sources'] = [source]
	data['metrics'] = metrics
	i = 1
	dimensionsDict = {}
	for dimension in dimensions:
		dimensionsDict[dimension] = i
		i += 1
	data['dimensions'] = dimensionsDict
	date1 = datetime.strptime(startDate,'%Y-%m-%d').strftime("%Y-%m-%d")
	date2 = (datetime.strptime(endDate,'%Y-%m-%d') + timedelta(1)).strftime("%Y-%m-%d")
	segments = []
	segmentsDict = {}
	segmentsDict['dateStart'] = "{0}T00:00:00+03:00".format(date1)
	segmentsDict['dateEnd'] = "{0}T00:00:00+03:00".format(date2)
	segmentsDict['filters'] = {}
	for filterKey, filterValue in filters.iteritems():
		segmentsDict['filters'][filterKey] = {}
		segmentsDict['filters'][filterKey]['type'] = 'DIMENSION'
		segmentsDict['filters'][filterKey]['ids'] = filterValue
	segments.append(segmentsDict)
	data['segments'] = segments
	return data

def getJSONOlapResponse(data):
	url = 'http://192.168.10.5:4000/api/OLAP/Plain'
	headers = {'Content-Type': 'application/json'}
	response = requests.post(url,data,headers=headers)
	return json.loads(response.text)

def transformOlapResponse(response,payload):
	data = []
	dimensionsList = [{'key': k, 'value': v} for k,v in payload['dimensions'].iteritems()]
	dimensionsList = sorted(dimensionsList, key=itemgetter('value'))
	for item in response:
		i = 0
		dataDict = {}
		for dimensionValue in item['dimensions']:
			dimensionName = dimensionsList[i]['key']
			dataDict[dimensionName] = dimensionValue
			i += 1
		metrics = item['value'][0]
		for k,v in metrics.iteritems():
			dataDict[k] = v
		data.append(dataDict)
	return data

# filters = {'campaignTypeId': ['1','2'], 'campaignExternalId': ['10784315']}
# source = 'direct_conversion'
# metrics = ['visits','shows','clicks','spent','cpaVisits']
# dimensions = ['dateDay','campaignExternalId','adExternalId']
# startDate = '2016-01-01'
# endDate = '2016-01-27'
# payload = createOlapPayload(source,metrics,dimensions,startDate,endDate,filters)
# response = getJSONOlapResponse(json.dumps(payload))
# data = transformOlapResponse(response,payload)
