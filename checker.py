# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
checkDatetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# Спрашиваем адрес сайта
site = raw_input(u'Введите адрес сайта: ')
# Читаем файл с проверками и записываем в датафрейм
df = pd.read_csv('C:\\Users\\aleksey.makarov\\Desktop\\2016-02\\Strategy_tree\\checkers_2.txt',sep='\t',encoding='utf8')
# Переименовываем первую колонку в 'checker'
df.rename(columns={'Unnamed: 0': 'checker'}, inplace=True)
# Для каждой проверки считаем количество каналов, на которые она влияет
for i in xrange(0,len(df)):
    df.loc[i,'channels_count'] = len(df.loc[i,][df.loc[i,] == 'v'].index)
# Сортируем проверки в порядке убывания количества каналов, на которые влияет проверка и сбрасываем индексы
df.sort('channels_count', ascending=False, inplace=True) 
df.reset_index(drop=True,inplace=True)
checkersInfo = []
deletedChannelInfo = []
channelsForUseInfo = []
# До тех пор пока количество проверок > 0 выполняем цикл:
while len(df) > 0: 
    question = df.loc[0,'checker']
    print '{0}'.format(question.encode('utf-8')) # Выводим первый из списка вопрос
    isOk = int(raw_input()) # Получаем результат проверки
    if isOk == 0: # Если проверка прошла успешно
        checkersInfo.append({'question':question,'status':isOk,'site':site,'datetime':datetime.now()})
        df.drop([0],inplace=True) # Удаляем из таблицы вопросов строку с проверкой
        df.reset_index(drop=True,inplace=True) # Сбрасываем индексы таблицы (чтобы вопросы начинались с нуля)
        for i in xrange(0,len(df)): # Для каждой проверки пересчитываем количество каналов, на которые она влияет
            df.loc[i,'channels_count'] = len(df.loc[i,][df.loc[i,] == 'v'].index)
        df = df[df.channels_count != 0] # Удаляем такие проверки, которые не влияют на какие-либо каналы
        df.reset_index(drop=True,inplace=True) # Сбрасываем индексы таблицы проверок (чтобы вопросы начинались с нуля)
        if len(df.columns) == 2 or len(df) == 0: # Если количество каналов = 0 или количество проверок = 0, то завершаем цикл
            break
    else: # Если проверка прошла неудачно
        checkersInfo.append({'question':question,'status':isOk,'site':site,'datetime':datetime.now()})
        deleted_channels = df.loc[0,][df.loc[0,] == 'v'].index # Получаем список каналов, которые затрагивает проверка
        for delChannel in list(deleted_channels):
            deletedChannelInfo.append({'deletedChannel':delChannel,'question':question,'site':site,'datetime':datetime.now()})
        df.drop(deleted_channels,axis=1,inplace=True) # Удаляем стоблцы каналов, не прошедшие проверку
        for i in xrange(0,len(df)): # Для каждой проверки пересчитываем количество каналов, на которые она влияет
            df.loc[i,'channels_count'] = len(df.loc[i,][df.loc[i,] == 'v'].index)
        df = df[df.channels_count != 0] # Удаляем такие проверки, которые не влияют на какие-либо каналы
        df.reset_index(drop=True,inplace=True) # Сбрасываем индексы таблицы проверок (чтобы вопросы начинались с нуля)
        if len(df.columns) == 2 or len(df) == 0: # Если количество каналов = 0 или количество проверок = 0, то завершаем цикл
            break
    print ' '
print 'Количество доступных каналов = ',len(df.columns)-2
if len(df.columns)-2 > 0:
    print 'Доступные каналы:'
for channelForUse in list(df.columns.drop([u'checker', u'channels_count'])):
    print channelForUse
    channelsForUseInfo.append({'channel':channelForUse,'site':site})
pd.DataFrame(checkersInfo).to_excel('D:\\{0}_{1}_checkersInfo.xlsx'.format(site,checkDatetime))
pd.DataFrame(deletedChannelInfo).to_excel('D:\\{0}_{1}_deletedChannelInfo.xlsx'.format(site,checkDatetime))
pd.DataFrame(channelsForUseInfo).to_excel('D:\\{0}_{1}_channelsForUseInfo.xlsx'.format(site,checkDatetime))