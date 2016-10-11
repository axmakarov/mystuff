from os import listdir
from os.path import isfile, join
mypath = 'C:\\Users\\aleksey.makarov\\Desktop\\2016-01\\2016-01-21\\calltracking\\'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
import pandas as pd
from pandas import ExcelWriter
site = 'umg-clinic'
writer = ExcelWriter('D:\\{0}.xlsx'.format(site))
dfs = []
for f in onlyfiles:
    if site in f:
        print f
        filepath = mypath + f
        df = pd.read_csv(filepath,sep=';',encoding='utf-8')
        if len(re.findall('calls',f)) > 0:
            df.to_excel(writer,'Calls')
        if len(re.findall('call.*\.csv',f)) > 0:
#             if 'UTMContent' in df.columns:
#                 df['UTMContent'] = df['UTMContent'].map(lambda x: x.decode('utf-8'))
            df.to_excel(writer,re.findall('call.*\.csv',f)[0].replace('.csv',''))
writer.save()