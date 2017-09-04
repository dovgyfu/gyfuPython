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

def chopNan(docType):
    if docType.endswith('nan'):
        dt = docType[:-3].strip()
    else:
        dt=  docType.strip()
        
    return dt
    
x = pd.read_csv(r'x:\Doc_Reports\Clean_Doc_List_2.csv', index_col=0)
x['DocType'] = x.DocType.map(chopNan)

allDocs = x

#x.to_csv(r'x:\Doc_Reports\Clean_Doc_List_2.csv')

freq = x.DocType.value_counts().to_frame()
print(freq) 

fnameDocs = r'y:\00_Done_Docs.csv'
df = pd.read_csv(fnameDocs)
df  = df [(df['ftype'] == 'GOOD') & (df['dup'] == "NODUP" ) & (df['ExtID'] == "MHNI")]

df.drop_duplicates(['DocID', 'MRN', 'DocDate', 'DocType'])
doneDocs = df
doneDocs = doneDocs[['MRN', 'DocDate', 'DocType']].reset_index().drop('index', 1)
doneDocs['MRN'] = doneDocs['MRN'].str[1:]
print(doneDocs.head())
allDocs = allDocs.drop('Patient Name', 1)
allDocs['MRN'] = allDocs['MRN'].astype('str')
print(allDocs.head())
numDone = len(doneDocs)
numDocs = len(allDocs)
docsMissing = numDocs - numDone
print("Number of Missing Docs=" + str(docsMissing))

allFreq =allDocs['DocType'].value_counts()
haveFreq = doneDocs['DocType'].value_counts()

print(allFreq)
print(haveFreq)
allFreq.head()
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

