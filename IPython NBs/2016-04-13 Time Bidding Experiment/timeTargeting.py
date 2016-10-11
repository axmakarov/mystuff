# -*- coding: utf-8 -*-
import allStuffHelper as ash
import pandas as pd

domain = 'doorlock.ru'
date1 = '2016-01-01'
date2 = '2016-09-11'

projectInfo = ash.getExtendedProjectInfo(domain,'Metrika')
goalsMetrics = ','.join(['ym:s:goal'+str(target['targetid'])+'visits' for target in ash.getCPATargetsByProjectID(projectInfo['projectid'])])
metrics = ','.join(['ym:s:visits',goalsMetrics])
dimensions='ym:s:dayOfWeek,ym:s:hour'
filters = "ym:s:UTMMedium=='direct'"
df = ash.getMetrikaReportInDataFrame(date1,date2,metrics,dimensions,projectInfo['token'],projectInfo['counterId'],filters,'lastsign')
df = ash.mergeCPAVisitsColumns(ash.dropTotalRow(df))
print 'Metrika Dataset Length:',len(df)
df.rename(columns={u'﻿"День недели визита"': 'dayofweek',
                        u'Час визита':'hour',
                        u'Визиты': 'visits'
                       }, inplace=True)
df.to_csv('data.csv',encoding='utf-8')
