import pandas as pd
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
mypath = 'C:\\Users\\aleksey.makarov\\Desktop\\2016-02\\VCG\\xmls\\'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
total_df = pd.DataFrame()
count = len(onlyfiles)
i = 1
for f in onlyfiles:
    print '{0} of {1}: {2}\t'.format(i,count,f),
    i += 1
    filepath = mypath + f
    with open(filepath,'r+') as f1:
        soup = BeautifulSoup(f1,'lxml')
    length = int(soup.report.stat.attrs['rows'])
    print 'Length = {0}\t'.format(length),
    if length == 0:
        print ''
        continue
    stats = []
    for tag in soup.report.stat.find_all('row'):
        stats.append(tag.attrs)
    print 'Len_check: {0}'.format(str(len(stats)==int(soup.report.stat.attrs['rows']))),
    campaignId = soup.report.campaignid.get_text()
    phrases = []
    for tag in soup.report.phrasesdict.find_all('phrase'):
        phrases.append(tag.attrs)
    df = pd.DataFrame(stats)
    df['campaignId'] = soup.report.campaignid.get_text()
    df2 = pd.DataFrame(phrases)
    df3 = pd.merge(df, df2, on='phraseid')
    df3.drop('type', axis=1, inplace=True)
    df3.rename(columns={'value': 'phrase'}, inplace=True)
    total_df = pd.concat([total_df,df3])
    print 'TotalDFLength: {0}'.format(len(total_df))