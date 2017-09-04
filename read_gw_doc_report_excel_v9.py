# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os

def parseMRN(docdf, orownum, count):
               
                patient = ''
                docType = ''
 
                while count < 4:
                    rownum = orownum + count
                    row = docdf.iloc[[rownum]] 
                    patient = patient +  str(row.iat[0, 1])
                    docType = docType + str(row.iat[0, 2])
#                    print(docType)
#                    print(patient)
                    m = re.match(r"(.+)\[(\d+)\]", patient)
                    if m == None:
                        count = count + 1   
                        
                    else:
                        MRN = m[2]
                        pName = m[1]
                        return [pName, MRN, docType]
#                row = docdf.iloc[[rownum]] 
                print("BAD ROWNUM= " + str(rownum))
                print(row)
                return ["NO Patient", "NOMRN", "NODOC"]
                                    
def parseDocType(docdf, startrow, count):
    count = 0
    docType = ''
#    print ("In parse doc Type")
    newdf = docdf[startrow:startrow+5]
#    print(len(newdf))
#    print(newdf)
    row = newdf.loc[[startrow]]
    docType = docType + str(row.iat[0, 2])    
    rowsleft = len(newdf)
    
    while rowsleft > 2 :
#        print("DocType=" + docType)
        nextrow = newdf.loc[[startrow+count+1]]
 #       print(type(nextrow))
        nextdate = nextrow.iat[0,0]
#        print(type(nextdate))
#        print(nextdate)
        if type(nextdate) == float:
#            print("NEXTDATE is NAN")
            docType = docType + " " + str(nextrow.iat[0, 2])    
            count = count + 1
            rowsleft = rowsleft - 1
        else:
#            print("NETDATE is NOT NAN")
#            print("Completed DocType: " + docType)
            return docType
            break
    return docType
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

def walk_doc_lists(directory_path):

    cldf = pd.DataFrame()
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '\\' + filename
#           print(filename)
           if (filename.startswith("gw_doc_report_012017_08242017")  and filename.endswith(".xls")):
                   print("reading: " + file_path)
                   df1 = pd.read_excel(file_path, sheetname='Sheet1', header=None, index=False)
                   df1 = df1[14:]
                   df1 = df1[[0, 2, 8, 9]]
                   df1 = df1.dropna(axis=0, how='all')
                   df1 = df1[df1[0] != "Note"]
                   df1 = df1[df1[0] != "Date"]
                   df1 = df1[df1[9] != "Page:"]
                   df1 = df1[df1[9] != "Date:"]
                   df1 = df1[df1[9] != "Time:"]
                   print(df1.head())
#docDelta = docDelta.rename(columns={'Count_y': 'totCount', 'Count_x': 'haveCount'})                   
                   cldf = cldf.append(df1)
    print(cldf.shape)
    return cldf

def getCleanDocList(docReport):
#    print("in getClean")
    docsDF = pd.DataFrame()
    i = 0
    totCount = 0
    twoLine = 0
#    docReport = docReport.head(120)
    print("START GET CLEAN")
    print(docReport.shape)
    for x in docReport.index:
#        print(x)       
        row = docReport.iloc[[x]]
    
        i = i + 1
        totCount = totCount + 1
#        print(row.shape)
        date = row.iat[0, 0]
        if i > 999:
            i = 0
            print("Count =" + str(totCount))
        if type(date) == str:
            docDate = valDate(date)
            if docDate != None:
                pMRN = parseMRN(docReport, x, 0)
#                if pMRN != None:
                pName = pMRN[0]
                MRN = pMRN[1]
#                docType = pMRN[2]
                pDocType = parseDocType(docReport, x, 0)
#                print(pDocType)
                newRow = pd.DataFrame([[docDate, MRN, pName, pDocType]])
#                print(newRow)
                docsDF = docsDF.append(newRow)
#                print(pMRN)
#               return(pMRN)
    return docsDF
def ckDate(date):
    if type(date) == 'str':
        return "string"
    else:
        return "date"
    
listDir = r'y:\MHNI_Data\\' 
pandawork = r'y:\Pandas_Work\\'
pandadata = r'y:\Pandas_Data\\'
rawDocReport = walk_doc_lists(listDir)

rawDocReport = rawDocReport.reset_index()

rawDocReport = rawDocReport[[0,2,8]]
t = getCleanDocList(rawDocReport).reset_index()

cleanDocList = t.reset_index()[[0, 1, 2, 3]]
cleanDocList = cleanDocList.rename(columns={0: 'DocDate', 1: "MRN", 2: "Patient Name", 3: "DocType" })
cleanDocList.to_csv(pandadata + 'Clean_Doc_List.csv')

oldDir = r'x:\Doc_Reports\\'
oldDocList = pd.read_csv(oldDir + 'Clean_Doc_List.csv')
oldDocList = oldDocList.drop('Unnamed: 0', axis=1)
newDocList = oldDocList.append(cleanDocList)

newDocList.to_csv(pandadata + 'gw_report_allDocs.csv', index=False)
mrnlist = newDocList.drop_duplicates(subset='MRN')[['MRN']]
mrnlist.to_csv(pandawork + "newMRNList.csv", index=False)
oldmrnlist =pd.read_csv(r'y:\Pandas_Work\chartswithDocs.csv')

#noMRN = t[1]   == "NOMRN"
#print(t[noMRN])
