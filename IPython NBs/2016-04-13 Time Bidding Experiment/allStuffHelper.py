# -*- coding: utf-8 -*-
import requests
import json
import psycopg2
import pandas as pd

def getVipProjectByDomain(domain):
    conn = psycopg2.connect("dbname='CRM' user='read_only' host='192.168.10.10' password='User_ro'")
    cur = conn.cursor()
    cur.execute("SELECT p.projectid, p.domain, p.status, p2.login, p2.password FROM project AS p INNER JOIN ProjectMetrikaData AS p2 ON p.UniqueId = p2.ProjectUniqueId WHERE domain=%s AND p.status<230 ORDER BY p.projectid", [domain])
    result = []
    rows = cur.fetchall()
    for row in rows:
        result.append(getVipProjectByRow(row))
    return result
def getVipProjectByRow(row):
    return {'projectid': row[0], 'domain': row[1], 'metrikalogin': row[3], 'metrikapassword': row[4]}

def getCPATargetsByProjectID(projectID):
    conn = psycopg2.connect("dbname='Cubo' user='read_only' host='192.168.10.8' password='User_ro'")
    cur = conn.cursor()
    cur.execute("SELECT targetstatus, targetid, targetname FROM metricstarget WHERE projectid=%s ORDER BY id DESC", [projectID])
    result = []
    rows = cur.fetchall()
    for row in rows:
        result.append(getCPATargetByRow(row))
    return result
def getCPATargetByRow(row):
    return {'targetstatus': row[0], 'targetid': row[1], 'targetname': row[2]}

def getGoalsByCounter(counterId,token):
    return requests.get('https://api-metrika.yandex.ru/management/v1/counter/{0}/goals?oauth_token={1}'.format(counterId,token)).text.encode('utf-8')

def getMetrikaReportInDataFrame(date1,date2,metrics,dimensions,token,counterId,filters,attribution):
    params = '&'.join(['dimensions={0}'.format(dimensions),
                       'metrics={0}'.format(metrics),
                       'date1={0}'.format(date1),
                      'date2={0}'.format(date2),
                      'ids={0}'.format(counterId),
                      'oauth_token={0}'.format(token),
                      'limit=100000',
                      'offset=1',
                      "filters={0}".format(filters),
                      'accuracy=full',
                      'attribution={0}'.format(attribution)])
    url = 'https://beta.api-metrika.yandex.ru/stat/v1/data.csv?'+params
    print url
    df = pd.read_csv(url,encoding='utf-8')
    return df

def mergeCPAVisitsColumns(df):
    col_list = [column for column in df.columns if u'Целевые визиты' in column]
    df['goal_visits'] = df[col_list].sum(axis=1)
    df.drop(col_list, axis=1, inplace=True)
    return df
def dropTotalRow(df):
    return df.drop(df.index[0]).reset_index(drop=True)

def getMetrikaCountersByToken(oAuthToken): # Получаем массив словарей со списком счетчиков для токена
    url = 'https://beta.api-metrika.yandex.ru/management/v1/counters?oauth_token={0}'.format(oAuthToken)
    r = requests.get(url)
    try:
        response = json.loads(r.text)
        counters = response['counters']
        return counters
    except:
        return '-1'

def getMetrikaCounterIDByDomain(counters, domain): # Получаем ID счетчика для домена
    counterID = []
    for counter in counters:
        try: # Иногда отваливается с ошибкой string indices must be integers. Возможное решение: вызывать несколько раз getMetrikaCountersByToken http://stackoverflow.com/questions/7293978/repeat-an-iteration-of-for-loop
            if domain in counter['site'] and counter['code_status'] == 'CS_OK':
                counterID.append(counter['id'])
        except:
            print 'getMetrikaCounterIDByDomain exception'
            continue
    return counterID

def GetToken(login,serviceType):
    if serviceType not in ['Metrika','Direct']:
        print 'Invalid service type'
        return None
    url = 'http://192.168.10.37:35678/TokenManagerService'
    payload = {'method':'GetToken','params':{'login':login.replace('@yandex.ru',''),'serviceType':serviceType}}
    r = requests.post(url,json.dumps(payload))
    data = json.loads(r.text)
    if len(data.keys()) == 1:
        print 'Invalid login'
        return None
    return data['result']['token']

def getExtendedProjectInfo(domain,serviceType):
    vipProjectInfo = getVipProjectByDomain(domain)[0]
    token = GetToken(vipProjectInfo['metrikalogin'],serviceType)
    if serviceType == 'Metrika':
        counters = getMetrikaCountersByToken(token)
        counterId = getMetrikaCounterIDByDomain(counters, domain)[0]
        vipProjectInfo['counterId'] = counterId
    vipProjectInfo['token'] = token
    return vipProjectInfo

def getMetrikaGoalMetrics(projectid):
    goalsMetrics = ','.join(['ym:s:goal'+str(target['targetid'])+'visits' for target in getCPATargetsByProjectID(projectid)])
    return goalsMetrics
