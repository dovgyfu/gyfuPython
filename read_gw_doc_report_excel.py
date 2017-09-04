# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
def valDate(date): 
        print("Validating Date: " + date)
        try:
            dtGood = True
            docDate = datetime.strptime(date, '%m/%d/%Y')
        except:
            dtGood=False

        if dtGood == True:
            
            pMRN = parseMRN(wFile, x, 0)
            if pMRN != None:
                pName = pMRN[0]
                MRN = pMRN[1]
            else:
                pName = row[2]
                MRN = "NOMRN"
                twoLine = twoLine + 1

def walk_doc_lists(directory_path, fname):

    cldf = pd.DataFrame()
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '\\' + filename
           print(filename)
           if (filename.startswith("gw_docs_2017")  and filename.endswith(".xls")):
                   print("reading: " + file_path)
                   df1 = pd.read_excel(file_path, sheetname='Sheet1', header=None, index=False)
                   df1 = df1[[0, 2, 8]]
                   df1 = df1.dropna(axis=0, how='all')
                   cldf = cldf.append(df1)
    print(cldf.shape)
    return cldf

def getCleanDocList(docReport):
    docsDF = pd.DataFrame()
    i = 0
    twoLine = 0
    docReport = docReport.head(100)

    for x in docReport.index:
        
        row = docReport.iloc[[x]]
    
        i = i + 1
#        print(row.shape)
        date = row.iat[0, 0]
#        print(date)
        valDate(date)

  
'''
                
            tRow = [{"docDate": docDate, "Patient": pName, "MRN": MRN}]
            rowDF = pd.DataFrame(tRow)
            docsDF = docsDF.append(rowDF)
                        
def parseMRN(csvList, rownum, count):
    
                patient = ''
                while count < 3:
                    row = csvList[rownum + count]                        
                    patient = patient + row[2]
                    m = re.match(r"(.+)\[(\d+)\]", patient)
                    if m == None:
                        count = count + 1
                        pass
                    else:
                        pName = patient
                        MRN = "NOMRN"
                        MRN = m[2]
                        pName = m[1]
                        return [pName, MRN]

print("===== Scanning the Documents Directory")
fnameDocs = r'y:\Robot\robot_assign.csv'

listDir = r'x:\Doc_reports'
rawDocReport = walk_doc_lists(listDir, fnameDocs)
rawDocReport = rawDocReport.reset_index()
rawDocReport = rawDocReport[[0, 2, 8]]
getCleanDocList(rawDocReport)

'''                       
                    
listDir = r'x:\MHNI_sample'

file_path = listDir + r"\ROBOT0_chart_list.xlsx"
status = pd.read_excel(file_path, sheetname='status',  header=None)
lastProcRow = status.iloc[0][1]
print(lastProcRow)
                                                                
filename = r'x:\MHNI_sample\gw_doc_report.csv'

    
    print("Tot records read=" + str(i))
    print("Doc Count=" + str(len(docsDF)))
    print("Two count=" + str(twoLine))
    docsDF = docsDF.reset_index()
    docsDF = docsDF[['docDate', 'MRN', 'Patient']]
    
    mrnGrp = docsDF.groupby(['MRN'])
    tf = mrnGrp.count()['docDate']
    tf = tf.rename(columns={'docDate': 'Count'})
    newF = tf.to_frame().reset_index()
    totNewMRN = len(newF)
    print(newF.head())
    totFiles = tf.sum()
    
    print(docsDF.head())
    print ("Total Docs since 5/15/17=" + str(totFiles) + " For " + str(totNewMRN) + " Charts")
    
    
    file = 'y:\\full_chart_doc_count.xlsx'
    xl = pd.ExcelFile(file)
    #print (xl.sheet_names)
    fullDocCount  = xl.parse('Sheet1')
    fullDocCount['PID'] = fullDocCount['PID'].fillna(0)
    fullDocCount['TEMP'] =  fullDocCount['PID'].astype('int')
    fullDocCount['MRN'] =  "A" + fullDocCount['TEMP'].astype('str')
    fullDoc = fullDocCount[['DocType','Count','MRN']]
    #totalDocCount = fullDocCount['Count'].sum()
    docCount = fullDoc['Count'].sum()
    print("Total Doc Count: " + str(docCount))
    fullDoc.MRN = fullDoc.MRN.str[1:]
    newDocDelta = pd.merge(newF, fullDoc, how='outer', on='MRN')
    print("Total Charts=" + str(len(docDelta)))
    
    haveDocs = pd.read_csv(r'y:\00_full_status.csv')
    combDelta = pd.merge
    '''