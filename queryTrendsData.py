# -*- coding: utf-8 -*-
import math
queriesTrendsData = [
[662,729,1308,1975,3843,5937,4380,2089,395,157,205,196,714,975,1475,2326,5139,7034,6896,3030,629,301,324,312],
[0,0,0,105,152,264,190,115,41,28,24,32,77,55,122,133,260,375,424,171,64,31,36,36],
[113,133,165,227,248,252,157,109,72,68,69,44,80,126,142,249,226,188,156,67,29,27,27,68],
[79,91,119,330,737,1315,1104,442,63,28,23,12,46,76,203,364,663,1338,934,367,49,24,29,35],
[0,16,19,114,224,102,18,9,6,1,0,0,0,71,0,273,222,82,20,12,38,24,38,79],
[10,29,13,22,3,0,0,0,7,1,0,0,0,0,4,26,0,0,0,0,0,0,56,52],
[140,107,35,9,5,0,12,94,76,154,110,112,115,78,19,0,0,0,35,112,254,557,689,393],
[21,31,19,2,0,0,0,0,0,0,0,0,17,58,32,0,0,0,0,0,15,38,36,59],
[523,420,263,136,73,56,69,84,174,233,331,609,686,679,305,109,80,84,86,283,316,324,475,911]]
newQueriesTrendsData = []
for queryTrendsData in queriesTrendsData: # Для каждого запроса
    firstYearSumm = 0
    for monthCount in xrange(0,12):
        firstYearSumm += queryTrendsData[monthCount] # Считаем сумму для первого года
    secondYearSumm = 0
    for monthCount in xrange(12,24):
        secondYearSumm += queryTrendsData[monthCount] # Считаем сумму для второго года
    growthFactor = float (secondYearSumm) / float (firstYearSumm) - 1.0
    queryTrendsData = [queryTrendsData[monthCount]*(1-(monthCount-12)*(growthFactor/12)) for monthCount in xrange(12,24)] # Выравниваем показатели запроса
    newQueriesTrendsData.append(queryTrendsData)
newQueriesTrendsData = [[MonthData-min(newQueryTrendsData) for MonthData in newQueryTrendsData ] if min(newQueryTrendsData) < 0 else newQueryTrendsData for newQueryTrendsData in newQueriesTrendsData] # Если после выравнивания в запросе получили отрицательные значения, то из каждого значения для данного запроса вычитаем минимальное значение
totals = [0,0,0,0,0,0,0,0,0,0,0,0]
for newQueryTrendsData in newQueriesTrendsData:
    for i in xrange(0,12):
        totals[i] += newQueryTrendsData[i] # Суммируем покаазатели всех запросов
totals = [total/min(totals) for total in totals] # Нормируем по минимальному значению
totals = [0.5*math.log(total)+1 for total in totals] # Сглаживаем по натуральному логарифму
totals = [total/(sum(totals)/12) for total in totals] # Нормируем по среднему значению