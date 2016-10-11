%run 'D:\dev\prod\allStuffHelper.py'
import pandas as pd
import psycopg2
import math
import numpy
from datetime import timedelta
from datetime import datetime
from pandas import ExcelWriter
import json,requests,time
from bs4 import BeautifulSoup
from pandas import ExcelWriter
import numpy as np

class DirectReport(object):
    """Get Direct Report"""

    def __init__(self, token, columns, campaignId, startDate, endDate):
        self._token = token
        self._url = 'https://api.direct.yandex.ru/live/v4/json/'
        self._columns = columns
        self._campaignId = campaignId
        self._startDate = startDate
        self._endDate = endDate

    def _createNewReportPayload(self):
        payload = {
        "method": "CreateNewReport",
        "token": self._token,
        "param": {
            "CampaignID": self._campaignId,
            "StartDate": self._startDate,
            "EndDate": self._endDate,
            "GroupByColumns": self._columns,
            "GroupByDate": "day",
            "TypeResultReport": "xml",
            "CompressReport": 0}
            }
        return payload

    def _createJsonUTF8Payload(self,payload):
        return json.dumps(payload, ensure_ascii=False).encode('utf8')

    def _createReport(self):
        payload = self._createJsonUTF8Payload(self._createNewReportPayload())
        return requests.post(self._url,payload).text

    def _getReportList(self):
        payload = self._createJsonUTF8Payload({
            "method": "GetReportList",
            "token": self._token
            })
        return requests.post(self._url,payload).text

    def _getReport(self,reportID):
        reportList = self._getReportList()
        reportItem = (item for item in json.loads(reportList)['data'] if item["ReportID"] == json.loads(reportID)['data']).next()
        if reportItem['StatusReport'] == 'Done':
            data = requests.get(reportItem['Url']).text
            return data
        else:
            return False

    def _deleteReport(self,reportID):
        payload = self._createJsonUTF8Payload({
            "method": "DeleteReport",
            "token": self._token,
            "param": reportID
            })
        return requests.post(self._url,payload).text

    def _getReportData(self):
        reportId = self._createReport()
        time.sleep(100)
        report = self._getReport(reportId)
        print self._deleteReport(json.loads(reportId)['data'])
        return report

class DirectReportProcessing(object):
    """Direct report data processing tasks: parse XML, create Pandas DataFrame"""

    def __init__(self, report):
        self._report = report
        self._data = BeautifulSoup(self._report,'lxml').report
        self._campaignId = self._data.campaignid.get_text()

    def _parseXML(self):
        length = int(self._data.stat.attrs['rows'])
        print 'Direct report length = {0}\t'.format(length)
        if length > 0:
            stats = []
            for tag in self._data.stat.find_all('row'):
                stats.append(tag.attrs)
            print 'Length check: {0}'.format(str(len(stats)==length))
        return stats

    def _createDataFrame(self):
        stats = self._parseXML
        df_stats = pd.DataFrame(stats)
        df_stats['campaignId'] = self._campaignId
        return self._castDataFrame(df_stats)

    def _castDataFrame(self,df):
        df['clicks'] = df['clicks'].astype(int)
        df['clicks_context'] = df['clicks_context'].astype(int)
        df['clicks_search'] = df['clicks_search'].astype(int)
        df['shows'] = df['shows'].astype(int)
        df['shows_context'] = df['shows_context'].astype(int)
        df['shows_search'] = df['shows_search'].astype(int)
        df['sum'] = df['sum'].astype(float)*30.0
        df['sum_context'] = df['sum_context'].astype(float)*30.0
        df['sum_search'] = df['sum_search'].astype(float)*30.0
        df['campaignId'] = df['campaignId'].astype(int)

def getMetrikaData (projectInfo,date1,date2):
    dimensions = 'ym:s:directID,ym:s:deviceCategory,ym:s:gender,ym:s:ageInterval'
    goalsMetrics = ','.join(['ym:s:goal'+str(target['targetid'])+'visits' for target in getCPATargetsByProjectID(projectInfo['projectid'])])
    otherMetrics = 'ym:s:visits,ym:s:bounceRate'
    metrics = ','.join([otherMetrics,goalsMetrics])
    filters = ""
    attribution = 'lastsign'
    metrikaData = getMetrikaReportInDataFrame(date1,date2,metrics,dimensions,projectInfo['token'],projectInfo['counterId'],filters,attribution)
    metrikaGoalsData = mergeCPAVisitsColumns(dropTotalRow(metrikaData))
    return metrikaGoalsData

def processMetrikaData (metrikaData):
    df.rename(columns={u'﻿"Кампания Яндекс.Директа"': 'campaignId',
                   u'Тип устройства':'device_type',
                   u'Пол': 'gender',
                   u'Возраст': 'age',
                  u'Визиты':'visits',
                  u'Отказы':'bounceRate'},
          inplace=True)
    df = df[~df[u'device_type'].isin([u'ТВ'])]
    df['bounces'] = df['visits']*df['bounceRate']
    df['conversion_rate'] = df['goal_visits']/df['visits']
    df['campaignId'] = df['campaignId'].str.replace('N-','').astype(int)
    df.replace(to_replace={'device_type':{u'ПК':'desktop',u'Смартфоны':'mobile',u'Планшеты':'tablet'},
                          'age':{u'младше 18 лет':'AGE_0_17',u'18‑24 года':'AGE_18_24',u'25‑34 года':'AGE_25_34',u'35‑44 года':'AGE_35_44',u'45 лет и старше':'AGE_45',u'Не определено':'AGE_UNKNOWN'},
                          'gender':{u'женский':'GENDER_FEMALE',u'мужской':'GENDER_MALE',u'Не определено':'GENDER_UNKNOWN'}},inplace=True)
    return df

def mergeDataFrames(metrikaData,directData):
    merged_df = pd.merge(metrikaData,directData,on=['age','device_type','gender','campaignId'],how='inner')
    merged_df['cpv'] = merged_df['sum']/merged_df['visits']
    print 'Check merged dataframe length:',len(metrikaData)==len(merged_df)
    return merged_df

def groupData(df):
    cleaned_df = df[~df['gender'].isin(['GENDER_UNKNOWN'])]
    cleaned_df = cleaned_df[~cleaned_df['age'].isin(['AGE_UNKNOWN'])]
    cleaned_df = cleaned_df[['campaignId','age','gender','sum','visits','goal_visits']].groupby(['campaignId','age','gender'],as_index=False).sum()
    return cleaned_df

class GenderAgeDataframe(object):
    """Calculate gender-age dataframe with bid adjustments"""

    def __init__(self,source_df):
        self._df = source_df

    def _checkSourceDataframe(self):
        if self._df['goal_visits'].sum() == 0:
            return False

    def _calculateGenderAgeDataframe(self):
        if not self._checkSourceDataframe():
            return pd.DataFrame()
        gender_age_df = self._df
        gender_age_df['conversed_cpa'] = gender_age_df['goal_visits']/gender_age_df['sum']
        gender_age_df['conversed_cpa'] = gender_age_df['conversed_cpa'].replace(np.inf, np.nan).fillna(0)
        gender_age_df['conversion_rate'] = gender_age_df['goal_visits']/gender_age_df['visits']
        gender_age_df['cpv'] = gender_age_df['sum']/gender_age_df['visits']
        gender_age_visits = gender_age_df['visits'].sum()
        gender_age_sum = gender_age_df['sum'].sum()
        gender_age_goal_visits = gender_age_df['goal_visits'].sum()
        gender_age_conversion_rate = gender_age_goal_visits/gender_age_visits
        gender_age_conversed_cpa = gender_age_goal_visits/gender_age_sum
        gender_age_conversed_cpa_std = gender_age_df['conversed_cpa'].std()
        gender_age_df['sqrt_sum'] = gender_age_df['sum'].apply(numpy.sqrt)
        gender_age_df['z_criteria'] = (gender_age_df['conversed_cpa'] - gender_age_conversed_cpa)/(gender_age_conversed_cpa_std/gender_age_df['sqrt_sum'])
        gender_age_df['z_criteria'] = gender_age_df['z_criteria'].replace(np.inf, np.nan).fillna(0)
        return gender_age_df

    def _calculateBidAdjsutemnts(self,gender_age_df,min_bid_adjustment,max_bid_adjustment):
        gender_age_df['min_bid_adj'] = min_bid_adjustment
        gender_age_df['max_bid_adj'] = max_bid_adjustment
        maximum_z_criteria = gender_age_df['z_criteria'].max()
        minimum_z_criteria = gender_age_df['z_criteria'].min()
        delta_z_criteria = maximum_z_criteria - minimum_z_criteria
        adjustment_step = (max_bid_adjustment-min_bid_adjustment)/delta_z_criteria
        gender_age_df['bid_adjustment'] = (gender_age_df['z_criteria'] + abs(minimum_z_criteria))*adjustment_step + min_bid_adjustment
        gender_age_df['new_visits'] = gender_age_df['visits']*(1+gender_age_df['bid_adjustment'])
        gender_age_df['new_cpv'] = gender_age_df['cpv']*(1+gender_age_df['bid_adjustment'])
        gender_age_df['new_sum'] = gender_age_df['new_visits']*gender_age_df['new_cpv']
        gender_age_df['new_goal_visits'] = gender_age_df['new_visits']*gender_age_df['conversion_rate']
        gender_age_df['new_conversed_cpa'] = gender_age_df['new_goal_visits']/gender_age_df['new_sum']
        gender_age_df['new_conversed_cpa'] = gender_age_df['new_conversed_cpa'].replace(np.inf, np.nan).fillna(0)
        return gender_age_df

    def _searchOptimalCalculation(self,gender_age_df):
        MAX_BID_ADJ = 119
        MIN_BID_ADJ = 6
        MAX_DIFFERENCE = 0.15
        optimalCalculations = []
        for min_bid_adjsutment in xrange(MIN_BID_ADJ,10):
            for max_bid_adjsutment in xrange(11,MAX_BID_ADJ+1):
                print min_bid_adjsutment/10.0,max_bid_adjsutment/10.0
                calculation = self._calculateBidAdjsutemnts(gender_age_df,min_bid_adjsutment/10.0,max_bid_adjsutment/10.0)
                if abs(calculation['sum']/calculation['new_sum']) < MAX_DIFFERENCE & abs(calculation['visits']/calculation['new_visits']) < MAX_DIFFERENCE:
                    optimalCalculations.append({'df':calculation,'new_goal_visits':calculation['new_goal_visits']})
        return optimalCalculations

    def _getBestCalculation(self,optimalCalculations):
        bestCalculation = max(optimalCalculations, key=lambda x:x['new_goal_visits'])
        return bestCalculation




project = u'stranao3.ru'
VipProjectInfo = getExtendedProjectInfo(project,'Metrika')
print VipProjectInfo
date1 = '2016-02-01'
date2 = '2016-07-25'
metrika_df = getMetrikaData(VipProjectInfo,date1,date2)
metrika_df = processMetrikaData(df)
directToken = GetToken('alexgrtula','Direct')
columns = ['clDemographics','clDeviceType']
excluded_campaigns = [9208736]
campaigns_list = [x for x in list(metrika_df['campaignId'].unique()) if x not in excluded_campaigns]
direct_stats = []
for campaignId in campaigns_list:
    print 'Create report: {0}'.format(campaignId)
    dr = DirectReport(directToken,columns,campaignId,date1,date2)
    reportData = dr._getReportData()
    drp = DirectReportProcessing(reportData)
    campaign_stats = drp._createDataFrame(drp._parseXML())
    direct_stats.append(campaign_stats)
bestCalcs = []
for direct_df in direct_stats:
    campaignId = direct_df['campaignId'][0]
    metrika_criteria_df = metrika_df[metrika_df['campaignId'] == campaignId]
    merged_df = groupData(mergeDataFrames(metrika_criteria_df,direct_df))
    gad = GenderAgeDataframe(merged_df)
    gender_age_df = gad._calcucateGenderAgeDataframe()
    optimalCalculations = gad.__searchOptimalCalculation(gender_age_df)
    bestCalculation = gad._getBestCalculation(optimalCalculations)
    bestCalcs.append(bestCalculation)



# Для каждого direct_stats получаем campaignId
# Выбираем данные по campaignId из metrika_df
# Мерджим выбранные из metrika_df данные с direct_stats (функция для мерджа)
# Убираем неизвестные данные (UNKNOWN) и группируем по campaignId, age, gender (функция для группировки)
# Рассчитываем для группированных данных gender_age_df (добавить обработку goals = 0)
# Рассчитывем gender_age_adj_df для gender_age_df (N вариантов)
# Находим лучший вариант
# Выводим данные лучшего варианта

def calcGenderAgeDfForCampaign(campaignDf):
    calc_gender_age_df['conversed_cpa'] = calc_gender_age_df['goal_visits']/calc_gender_age_df['sum']
    calc_gender_age_df['conversed_cpa'] = calc_gender_age_df['conversed_cpa'].replace(np.inf, np.nan).fillna(0)
    calc_gender_age_df['conversion_rate'] = calc_gender_age_df['goal_visits']/calc_gender_age_df['visits']
    calc_gender_age_df['cpv'] = calc_gender_age_df['sum']/calc_gender_age_df['visits']
    calc_gender_age_visits = calc_gender_age_df['visits'].sum()
    calc_gender_age_sum = calc_gender_age_df['sum'].sum()
    calc_gender_age_goal_visits = calc_gender_age_df['goal_visits'].sum()
    calc_gender_age_conversion_rate = calc_gender_age_goal_visits/calc_gender_age_visits
    try:
        calc_gender_age_conversed_cpa = calc_gender_age_goal_visits/calc_gender_age_sum
    except ZeroDivisionError:
        calc_gender_age_conversed_cpa = 0
    calc_gender_age_conversed_cpa_std = calc_gender_age_df['conversed_cpa'].std()
    try:
        calc_gender_age_cpa = calc_gender_age_sum/calc_gender_age_goal_visits
    except ZeroDivisionError:
        calc_gender_age_cpa = 0
    calc_gender_age_df['sqrt_sum'] = calc_gender_age_df['sum'].apply(numpy.sqrt)
    calc_gender_age_df['z_criteria'] = (calc_gender_age_df['conversed_cpa'] - calc_gender_age_conversed_cpa)/(calc_gender_age_conversed_cpa_std/calc_gender_age_df['sqrt_sum'])
    calc_gender_age_df['z_criteria'] = calc_gender_age_df['z_criteria'].replace(np.inf, np.nan).fillna(0)
    return calc_gender_age_df

def calcGenderAgeDf(merged_df):
    campaign_dfs = []
    for campaignId in merged_df['campaignId'].unique():
        calc_gender_age_df = calcGenderAgeDfForCampaign(merged_df[merged_df['campaignId'] == campaignId])
        campaign_dfs.append(calc_gender_age_df)
    return campaign_dfs

def calcBidAdjustments(campaign_dfs,ga_min_bid_adjustment,ga_max_bid_adjustment):
    calculated_dfs = []
    for calc_gender_age_df in campaign_dfs:
        calc_gender_age_df['min_bid'] = ga_min_bid_adjustment
        calc_gender_age_df['max_bid'] = ga_max_bid_adjustment
        ga_maximum_z_criteria = calc_gender_age_df['z_criteria'].max()
        ga_minimum_z_criteria = calc_gender_age_df['z_criteria'].min()
        ga_delta_z_criteria = ga_maximum_z_criteria - ga_minimum_z_criteria
        ga_adjustment_step = (ga_max_bid_adjustment-ga_min_bid_adjustment)/ga_delta_z_criteria
        calc_gender_age_df['bid_adjustment'] = (calc_gender_age_df['z_criteria'] + abs(ga_minimum_z_criteria))*ga_adjustment_step + ga_min_bid_adjustment
        for i in xrange(0,len(calc_gender_age_df)):
            if (calc_gender_age_df.loc[i,'age'] == 'AGE_UNKNOWN') or (calc_gender_age_df.loc[i,'gender'] == 'GENDER_UNKNOWN'):
                calc_gender_age_df.loc[i,'bid_adjustment'] = 1
        calc_gender_age_df['new_visits'] = calc_gender_age_df['visits']*calc_gender_age_df['bid_adjustment']
        calc_gender_age_df['new_cpv'] = calc_gender_age_df['cpv']*calc_gender_age_df['bid_adjustment']
        calc_gender_age_df['new_sum'] = calc_gender_age_df['new_visits']*calc_gender_age_df['new_cpv']
        calc_gender_age_df['new_goal_visits'] = calc_gender_age_df['new_visits']*calc_gender_age_df['conversion_rate']
        calc_gender_age_df['new_conversed_cpa'] = calc_gender_age_df['new_goal_visits']/calc_gender_age_df['new_sum']
        calc_gender_age_df['new_conversed_cpa'] = calc_gender_age_df['new_conversed_cpa'].replace(np.inf, np.nan).fillna(0)
        calc_gender_age_new_visits = calc_gender_age_df['new_visits'].sum()
        calc_gender_age_new_sum = calc_gender_age_df['new_sum'].sum()
        calc_gender_age_new_goal_visits = calc_gender_age_df['new_goal_visits'].sum()
        try:
            calc_gender_age_new_conversion_rate = calc_gender_age_new_goal_visits/calc_gender_age_new_visits
        except ZeroDivisionError:
            calc_gender_age_new_conversion_rate = 0
        try:
            calc_gender_age_new_conversed_cpa = calc_gender_age_new_goal_visits/calc_gender_age_new_sum
        except ZeroDivisionError:
            calc_gender_age_new_conversed_cpa = 0
        calc_gender_age_new_conversed_cpa_std = calc_gender_age_df['new_conversed_cpa'].std()
        try:
            calc_gender_age_new_cpa = calc_gender_age_new_sum/calc_gender_age_new_goal_visits
        except ZeroDivisionError:
            calc_gender_age_new_cpa = 0
        calculated_dfs.append(calc_gender_age_df)
    return calculated_dfs

MAX_BID_ADJ = 119
MIN_BID_ADJ = 6
dfs = []
dfs1 = calcGenderAgeDf(merged_df)
for min_bid_adjsutment in xrange(MIN_BID_ADJ,10):
    for max_bid_adjsutment in xrange(11,MAX_BID_ADJ+1):
        print min_bid_adjsutment/10.0,max_bid_adjsutment/10.0
        dfs2 = calcBidAdjustments(dfs1,min_bid_adjsutment/10.0,max_bid_adjsutment/10.0)
        dfs.append(pd.concat(dfs2))

final_df = pd.concat(dfs)
