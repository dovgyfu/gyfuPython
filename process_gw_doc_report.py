# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os

def valDate(date): 
#        return str(date)
#        print("Validating Date: " + date)
        try:
#            print(date)
            dtGood = True
            docDate = datetime.strptime(date, '%m/%d/%Y')
        except:
            dtGood=False

        if dtGood == True:
#            print(docDate)
            return docDate
        else:
            return None
def valDate2(date): 
#        return str(date)
#        print("Validating Date: " + date)
        try:
#            print(date)
            dtGood = True
            docDate = datetime.strptime(date, '%Y-%m-%d')
        except:
            dtGood=False

        if dtGood == True:
#            print(docDate)
            return docDate
        else:
            return None        
def formatDate(date):
    outDate = datetime.strftime(date, '%m/%d/%Y')
    print(type(date))
    print(date)
    return outDate
def chopNan(docType):

    if docType.endswith('nan'):
        dt = docType[:-3].strip()
    else:
        dt=  docType.strip()
        
    return dt
    
x = pd.read_csv(r'x:\Doc_Reports\Clean_Doc_List_2.csv', index_col=0)
x['DocType'] = x.DocType.map(chopNan)

allDocs = x
del x

freq = allDocs.DocType.value_counts().to_frame().reset_index().rename(columns=
                                   {"index": "DocType",
                                   "DocType": "Freq"})
#print(freq) 
del freq

fnameDocs = r'y:\00_Done_Docs.csv'
df = pd.read_csv(fnameDocs)
df  = df [(df['ftype'] == 'GOOD') & (df['dup'] == "NODUP" ) & (df['ExtID'] == "MHNI")]

df.drop_duplicates(['DocID', 'MRN', 'DocDate', 'DocType'])
doneDocs = df
del df
#doneDocs = doneDocs[['MRN', 'DocDate', 'DocType']].reset_index().drop('index', 1)
doneDocs = doneDocs.reset_index().drop('index', 1)
doneDocs['MRN'] = doneDocs['MRN'].str[1:]
doneDocs['count_Done'] = 1
ddAllC = doneDocs.copy()
ddAllC.DocDate = ddAllC.DocDate.map(valDate)
doneDocs = doneDocs[['MRN', 'DocDate', 'DocType', 'count_Done']].reset_index().drop('index', 1)

doneDocs.to_csv(r'y:\000_Clean_Done_Docs.csv', index=False)



grpDone = doneDocs.groupby(['MRN', 'DocDate', 'DocType'])
countDone = grpDone.sum()
sumDone = countDone.reset_index().sort_values('count_Done', ascending=False)
sumDone['DocDate'] = sumDone['DocDate'].map(valDate)
del countDone
#print(doneDocs.head())
allDocs = allDocs.drop('Patient Name', 1)
allDocs['MRN'] = allDocs['MRN'].astype('str')

allDocs['count_All'] = 1
allDocs.DocDate = allDocs.DocDate.map(valDate2)

allDocs.to_excel(r'y:\000_AllDocs.xlsx')
outerMatch = pd.merge(allDocs, ddAllC, how='outer', on=['MRN', 'DocDate', 'DocType']).fillna(0)

outer9440 = outerMatch[outerMatch.MRN == '9440']

outer9440['Delta'] = outer9440['count_All'] - outer9440['count_Done']
NM9440 = outer9440[outer9440['Delta'] != 0]

grpAll = allDocs.groupby(['MRN', 'DocDate', 'DocType'])
countAll = grpAll.sum()
sumAll = countAll.reset_index().sort_values('count_All', ascending=False)
sumAll['DocDate'] = sumAll['DocDate'].map(valDate2)
m = pd.merge(sumAll, sumDone, how='outer', on=['MRN', 'DocDate', 'DocType'])
m = m.fillna(0)
m['Delta'] = m['count_All'] - m['count_Done']

matchDocs = m
del m
misMatch = matchDocs[matchDocs['Delta'] != 0]
ng = misMatch.groupby('MRN').count().sum()

#print(allDocs.head())
numDone = len(doneDocs)
numDocs = len(allDocs)
docsMissing = numDocs - numDone
print("Total Done Docs= " + str(numDone))
print("Total Docs= " + str(numDocs))

print("Number of Missing Docs=" + str(docsMissing))

allFreq =allDocs['DocType'].value_counts()
haveFreq = doneDocs['DocType'].value_counts()

#print(allFreq)
#print(haveFreq)

allFreq = allFreq.reset_index()
haveFreq = haveFreq.reset_index()

haveFreq = haveFreq.rename(columns={'DocType': 'Count_Have', 'index': 'DocType'})
allFreq = allFreq.rename(columns={'DocType': 'Count_All', 'index': 'DocType'})
haveFreq = haveFreq.fillna(0)
allFreq = allFreq.fillna(0)
#print(haveFreq.head())
#print(allFreq.head())
deltadf = pd.merge(allFreq, haveFreq, how='outer', on='DocType')
deltadf = deltadf.fillna(0)
deltadf['Count_Have'] = deltadf['Count_Have'].astype('int')
deltadf['Count_All'] = deltadf['Count_All'].astype('int')

deltadf['MissingDocs'] = deltadf['Count_All'] - deltadf['Count_Have']
deltadf = deltadf[deltadf['Count_All'] > 0]
#print(deltadf.head(20))
deltadf.to_csv(r'x:\Doc_Reports\doc_by_type.csv')

