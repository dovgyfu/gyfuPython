# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os

def parseMRN(docdf, rownum, count):
#                print("In ParseMRN: " + str(rownum))
                patient = ''
                rownum = rownum + count
                row = docdf.iloc[[rownum]] 
 #               print(row)
                patient = row.iat[0, 1]
#                print(patient)
                m = re.match(r"(.+)\[(\d+)\]", patient)
                if m == None:
                    count = count + 1
                    return None
                else:
                    MRN = m[2]
                    pName = m[1]
                    return [pName, MRN]

                
'''
                while count < 1:
                    row = docdf.iloc[[count]] 
                    print(row)
                    patient = row.iat[0, 1]
                    print(patient)
                    count = count + 1
'''                    
'''                 
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
'''
def valDate(date): 
#        print("Validating Date: " + date)
        try:
            dtGood = True
            docDate = datetime.strptime(date, '%m/%d/%Y')
        except:
            dtGood=False

        if dtGood == True:
#            print(docDate)
            return docDate
        else:
            return None
'''            
            pMRN = parseMRN(wFile, x, 0)
            if pMRN != None:
                pName = pMRN[0]
                MRN = pMRN[1]
            else:
                pName = row[2]
                MRN = "NOMRN"
                twoLine = twoLine + 1
'''
def walk_doc_lists(directory_path):

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
#    print("in getClean")
    docsDF = pd.DataFrame()
    i = 0
    twoLine = 0
#    docReport = docReport.head(100)

    for x in docReport.index:
#        print(x)       
        row = docReport.iloc[[x]]
    
        i = i + 1
#        print(row.shape)
        date = row.iat[0, 0]
        
        if type(date) == str:
            docDate = valDate(date)
            if docDate != None:
                pMRN = parseMRN(docReport, x, 0)
                if pMRN != None:
                    pName = pMRN[0]
                    MRN = pMRN[1]
                    newRow = pd.DataFrame([[docDate, MRN, pName]])
#                    print(newRow)
                    docsDF = docsDF.append(newRow)
#                print(pMRN)
#               return(pMRN)
    return docsDF

listDir = r'x:\Doc_reports'
rawDocReport = walk_doc_lists(listDir)
rawDocReport = rawDocReport.reset_index()
rawDocReport = rawDocReport[[0, 2, 8]]
t =  getCleanDocList(rawDocReport).reset_index()[[0, 1, 2]]
print(t)
'''
docdf = rawDocReport.head(100)
count = 18
row = docdf.iloc[[count]] 
print(row)
patient = row.iat[0, 1]
print(patient)
count = count + 1
'''

