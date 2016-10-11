import json,requests,time
import pandas as pd
from bd4 import BeautifulSoup

URL = 'https://api.direct.yandex.ru/live/v4/json/'
TOKEN = "cc8fb959428d401a98ab953b75693f2e"

def createNewReportPayload(campaignID,startDate,endDate):
   payload = {
      "method": "CreateNewReport",
      "token": TOKEN,
      "param": {
         "CampaignID": campaignID,
         "StartDate": startDate,
         "EndDate": endDate,
         "GroupByColumns": ['clDate','clPage','clGeo','clPhrase','clStatGoals','clGoalConversionsNum','clPositionType','clImage','clAveragePosition','clDeviceType'],
         "GroupByDate": "day",
         "TypeResultReport": "xml",
         "CompressReport": 0,
      }
   }
   return payload

def createJsonUTF8Payload(payload):
   return json.dumps(payload, ensure_ascii=False).encode('utf8')

def createReport(campaignID):
   payload = createJsonUTF8Payload(createNewReportPayload(campaignID))
   return requests.post(URL,payload).text

def getReportList():
   payload = createJsonUTF8Payload({
   "method": "GetReportList",
   "token": TOKEN
   })
   return requests.post(URL,payload).text

def getReport(reportID):
   reportList = getReportList()
   reportItem = (item for item in dicts if item["ReportID"] == reportID).next()
   if reportItem['StatusReport'] == 'Done':
      data = requests.get(reportItem['Url']).text
      filename = reportItem['Url'].split('/')[-1]
      with open('D:\\direct_data\\xmls\\{0}'.format(filename),'wb') as f1:
         print >>f1, data
      return True
   else:
      return False

def deleteReport(reportID):
   payload = createJsonUTF8Payload({
   "method": "DeleteReport",
   "token": TOKEN
   "param": reportID
})
   return requests.post(URL,payload).text






