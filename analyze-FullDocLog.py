# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
pandaData = r'y:\Pandas_Data\\'
pandaWork = r'y:\Pandas_Work\\'

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
def mapSize(size):
    if size == 'nosize':
        return "UnSigned"
    else:
        return "Signed"
def mapSign(signed):
    if signed == 'Signed':
        return 1
    else:
        return 0
allLog = pd.read_csv(pandaData + 'all_log.csv', header=None, dtype={4: 'str'})

fullDocLog = allLog
fullDocLog = fullDocLog.rename(columns={5: 'DocID',
                                        4: 'DocSize',
                                        6: 'DocFormat',
                                        7: 'DocCreateDate',
                                        8: 'DocType',
                                        9: 'DocProvider',
                                        10: 'DocModDate',
                                        11: 'DocSignedBy',
                                        12: 'DocTitle',
                                        0:  'CapDate',
                                        1:  'CapTime',
                                        2:  'Robot',
                                        3:  'MRN'
                                        })
fullDocLog['docCreateDTTM'] = fullDocLog.DocCreateDate.map(valDate)   
fullDocLog['docModDTTM'] = fullDocLog.DocModDate.map(valDate)   
fullDocLog[['MRN', 'DocID']] = fullDocLog[['MRN', 'DocID']].astype('str')
fullDocLog['Signed'] = fullDocLog.DocSize.map(mapSize)
fullDocLog['SignCount'] = fullDocLog.Signed.map(mapSign)
fullDocLog['fdlCount'] = 1
fullDocLog['DocCategory'] = 'Clinical'
fullDocLog.to_csv(pandaData + "fullDocLog.csv", index=False)
#del allLog
'''
srtFDL = fullDocLog.sort_values(['MRN', 'DocID'])[['MRN', 'DocID']]
srtFDL['count'] = 1
docgrp = srtFDL.groupby(['DocID', 'MRN'])
tsum = docgrp.sum()
tsum = tsum.reset_index()
tsum['count'] = 1
docg2 = tsum.groupby(['DocID']) 
docidsum = docg2.sum().reset_index()
numdocs = len(docidsum)
print("Total Number of unique Doc ID=" + str(numdocs))
dupDocID = docidsum[docidsum['count'] > 1]
print("Number of DocID in more than One MRN=" + str(len(dupDocID)))

mrngrp = tsum.groupby(['MRN'])
mrnsum = mrngrp.sum().reset_index()

doneDocList = pd.read_csv(pandaData + "doneDocList.csv",dtype={'DocID': 'str'})

docLogtoDone = pd.merge(fullDocLog, doneDocList, how='outer',  on='DocID').fillna(0)

docLogtoDone.to_csv(pandaData + "docLogtoDone.csv", index=False)
fdl = docLogtoDone[docLogtoDone['fdlCount'] == 1]

sumDone = fdl[['MRN_x', 'DocID', 'DocCreateDate', 'DocModDate', 
                        'DocType_x', 'DocSize', 'DocFormat', 'Signed',
                        'fdlCount', 'done_count', 'SignCount', 'File', 'DocTitle' ]]
sumDone = sumDone.rename(columns={'MRN_x': 'MRN', 'DocType_x': 'DocType', 'fdlCount': 'Greenway_Count'})
sumDone['todo_Count'] = sumDone['SignCount'] - sumDone['done_count']
totDocs = len(sumDone)
print("Total Docs after Merge=" + str(totDocs))
sumDone.to_csv(pandaData + "Full_Greenway_Clinical_DocList.csv", index=False)
sgrp = sumDone.groupby(['MRN'])
sumbyMRN = sgrp.sum()
sumbyMRN.to_excel(pandaData + "sumbyMRN.xlsx")
todoList = sumDone[sumDone['todo_Count'] == 1]

todoList['pyDocDate'] = todoList.DocCreateDate.map(valDate)
todoList = todoList[['MRN', 'DocID', 'DocType', 'DocCreateDate', 'pyDocDate']]
todoList.to_excel(pandaData + "newROBOT.DocSelcfg.xlsx",index=False,header=None)
missingDoc = todoList

missingDoc = missingDoc.sort_values(['MRN', 'DocType', 'pyDocDate', 'DocID'],
                                    ascending=[True, True, False, True])
missingDoc.to_excel(pandaData + 'ROBOTX_docSel.xlsx', sheet_name='doc_list', index=False, header=False)


tgrp = allLog.groupby('MRN')
byMRN = tgrp.count()
byMRN = byMRN.reset_index()[['MRN', 0]]
haveMRN = byMRN
haveMRN['have_count'] = 1
haveMRN = haveMRN.drop_duplicates(subset='MRN')
haveMRN['MRN'] = haveMRN['MRN'].astype('str')
'''