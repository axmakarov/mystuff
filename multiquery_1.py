%run 'C:\dev\prod\metrikaHelper.py'
import pandas as pd
import psycopg2

def getVipProjectByDomain(domain):
    conn = psycopg2.connect("dbname='Cubo' user='read_only' host='192.168.10.8' password='User_ro'")
    cur = conn.cursor()
    cur.execute("SELECT projectid, domain, statisticlogin, statisticpassword FROM vipproject WHERE domain=%s ORDER BY id DESC LIMIT 1", [domain])
    result = []
    rows = cur.fetchall()
    for row in rows:
        result.append(getVipProjectByRow(row))
    return result

def getVipProjectByRow(row):
    return {'projectid': row[0], 'domain': row[1], 'metrikalogin': row[2], 'metrikapassword': row[3]}

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

def createMetrikaUrl(VipProjectInfo,metrikaCredentials):
    goalsMetrics = ','.join(['ym:s:goal'+str(target['targetid'])+'visits' for target in getCPATargetsByProjectID(VipProjectInfo[0]['projectid'])])
    otherMetrics = 'ym:s:visits'
    metrics = ','.join([otherMetrics,goalsMetrics])
    dimensions='ym:s:userIDHash,ym:s:dateTime,ym:s:UTMSource,ym:s:UTMMedium,ym:s:UTMContent,ym:s:UTMTerm'
    date1 = '2016-01-01'
    date2 = '2016-03-01'
    token = metrikaCredentials['Token']
    counterId = metrikaCredentials['counterID'][0]
    params = '&'.join(['dimensions={0}'.format(dimensions),
                       'metrics={0}'.format(metrics),
                       'date1={0}'.format(date1),
                      'date2={0}'.format(date2),
                      'ids={0}'.format(counterId),
                      'oauth_token={0}'.format(token),
                      'limit=10000',
                      'offset=1',
                      "filters=ym:s:UTMSource=='cubo'"])
    url = 'https://beta.api-metrika.yandex.ru/stat/v1/data.csv?'+params
    return url


