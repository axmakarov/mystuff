# -*- coding: utf-8 -*-
from bottle import route, run, request
import httplib
import urllib
import json

#Идентификатор приложения
client_id = '26258f7a864c4056a3b86beafe30435b'
#Пароль приложения
client_secret = 'f373c37153274761a6a41e793c0ab46b'

    #Если скрипт был вызван с указанием параметра "code" в URL,
    #то выполняется запрос на получение токена
code = '7976331'
        #Формирование параметров (тела) POST-запроса с указанием кода подтверждения
query = {
    'grant_type': 'authorization_code',
    'code': code,
    'client_id': client_id,
    'client_secret': client_secret,
}
query = urllib.urlencode(query)

        #Формирование заголовков POST-запроса
header = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

#Выполнение POST-запроса и вывод результата
connection = httplib.HTTPSConnection('oauth.yandex.ru')
connection.request('POST', '/token', query, header)
response = connection.getresponse()
result = response.read()
connection.close()
        
        #Токен необходимо сохранить для использования в запросах к API Директа
print json.loads(result)['access_token']
