# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
pandaData = r'y:\Pandas_Data\\'
def parseMRN(docdf, orownum, count):
#                return    ["A", "B", "C"]          
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
#    return ["A", "B", "C"]
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

def read_docReport(file_path):

       cldf = pd.DataFrame()
       print("reading: " + file_path)
       df1 = pd.read_excel(file_path, sheetname='Sheet1', header=None, index=False)
       df1 = df1[14:]
       df1 = df1[[0, 2, 8, 9]]
       df1 = df1.dropna(axis=0, how='all')
       '''
       df1 = df1[df1[0] != "Note"]
       df1 = df1[df1[0] != "Date"]
       df1 = df1[df1[9] != "Page:"]
       df1 = df1[df1[9] != "Date:"]
       df1 = df1[df1[9] != "Time:"]
       '''
       cldf = cldf.append(df1)
       print(cldf.shape)
       return cldf

def walk_doc_lists(directory_path):

    cldf = pd.DataFrame()
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '\\' + filename
#           print(filename)
           if (filename.startswith("gw_docs_")  and filename.endswith(".xls")):
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
#            '''
            if docDate != None:
                pMRN = parseMRN(docReport, x, 0)
                pName = pMRN[0]
                MRN = pMRN[1]
                pDocType = parseDocType(docReport, x, 0)
#                newRow = pd.DataFrame([[docDate, MRN, pName, pDocType]])
#                docsDF = docsDF.append(newRow)
#            '''
#                return(pMRN)
    return docsDF
def write_cfg(robot, list):
    if len(list) > 0:
        xlFile =  r'y:\Robot\\' + robot + "_cfg2a.xlsx"
        print(xlFile)
        df = pd.DataFrame(list)
#        df.to_excel(xlFile, sheet_name="chart_list", header=False)
        status= [["LastRow", -1, 0]]
        st = pd.DataFrame(status)
        xlwtr = pd.ExcelWriter(xlFile, engine='xlsxwriter')
        df.to_excel(xlwtr, sheet_name="chart_list", header=False,index=False)

        st.to_excel(xlwtr, sheet_name='status',header=False,index=False)
        xlwtr.save()
        xlwtr.close()
        
def parse_DocDate(x):
    date = x.split(":")[1].strip()
    return date
def parse_DocType(x):
    doctype = x.split(":")[1].strip()
    return doctype
def parse_DocProvider(x):
    docprovider = x.split(":")[1].strip()
    return docprovider
def parse_ModDate(x):
    docModdt = "NoDocModDt"
    modby = "NoModBy"
    m = re.match(r'DocModDate:(.*)ModBy:(.*)',x)
    if m!= None:
        docModdt = m[1].strip()
        modby = m[2].strip()
    return [docModdt, modby]
def parse_DocTitle(x):
    m = re.match(r'DocTitle:(.*)-:-', x)
    if m != None:
        DocTitle= m[1].strip()
        return DocTitle
    else:
        return "NOTITLE"
def read_rawLog(dir, robot):
#    print ("Processing: " + robot)
    global allLog
    outList = []
#    fname = r'y:\Robot_Logs\\' + robot + 'doclist.txt'
    fname = r'y:\Robot_Logs\\' + 'test.txt'

    print("Processing: " + fname)
    with open(fname) as f:
        for line in f:
            pattern = r'(.+)docinfo:(.*):edinfo:,(.*)'
            m = re.match(pattern, line)
            part1 = m[1]
            part2 = m[2]
            part3 = m[3]
            print("p1=" + part1)
            print("p2=" + part2)
            print("p3=" + part3)
            m = re.match(r'(.+) (.+) (.+) (.+) MRN:.*(\d{4})', part1)
            if m != None:
                logDate = m[1]
                logTime = m[2]
                robot = m[3]
                MRN = m[5]
    #            print(logDate + " " + logTime + " " + robot)
    #            print("MRN=" + MRN)
            docInfo =  part2.split("-:-")
            docSize = "nosize"
            docID = "noDocID"
            docfType = "nodocftype"
            
            for x in docInfo:
                kv = x.split(":")
                key = kv[0].strip()
                value = kv[1].strip()
                if key.startswith("Document ID"):
                    docID = value
                elif key.startswith("Size"):
                    docSize = value
                elif key.startswith('File Type'):
                    docfType = value
    #        print(part3)
            fields = part3.split(',')
            for x in fields:
                if x.startswith('DocDate:'):
                    docDate = parse_DocDate(x)
                elif x.startswith('DocType:'):
                    docType = parse_DocType(x)
                elif x.startswith('DocProvider:'):
                    docProvider = parse_DocProvider(x)
                elif x.startswith('DocModDate:'):
                    (docModDate, ModBy) = parse_ModDate(x)
                elif x.startswith('DocTitle:'):
                    DocTitle = parse_DocTitle(x)
    
            outRec = [logDate, logTime, robot, MRN, docSize, docID, docfType,
                      docDate,docType,docProvider,docModDate,ModBy,DocTitle]
            outList = outList + [outRec]
#            print("outlistlen=" + str(len(outList)) )
    #        break 
    print("outlistlen=" + str(len(outList)) )
    clinicalDocDF = pd.DataFrame(outList) 
    allLog = allLog.append(clinicalDocDF)

#    return clinicalDocDF
allLog = pd.DataFrame()
dirname = r'y:\Robot_Logs\\'
read_rawLog(dirname, "ROBOT0")
'''
allLog = pd.DataFrame()

read_rawLog(dirname, "ROBOT0")
read_rawLog(dirname, "ROBOT1")
read_rawLog(dirname, "ROBOT2")
read_rawLog(dirname, "ROBOT3")
read_rawLog(dirname, "ROBOT4")
read_rawLog(dirname, "ROBOT5")
read_rawLog(dirname, "ROBOT7")
read_rawLog(dirname, "ROBOT8")

allLog = allLog.rename(columns={3: 'MRN'})

tgrp = allLog.groupby('MRN')
byMRN = tgrp.count()
byMRN = byMRN.reset_index()[['MRN', 0]]
totMRN = mrnlist
totMRN['tot_count'] = 1
totMRN['MRN'] = totMRN['MRN'].astype('str')
totMRN = totMRN.drop_duplicates(subset='MRN')
haveMRN = byMRN
haveMRN['have_count'] = 1
haveMRN = haveMRN.drop_duplicates(subset='MRN')
haveMRN['MRN'] = haveMRN['MRN'].astype('str')
mrncomp = pd.merge(totMRN, haveMRN, how='outer', on='MRN')
mrncomp = mrncomp.fillna(0)[['MRN', 'tot_count', 'have_count']].reset_index()
del mrncomp['index']
mrncomp = mrncomp.sort_values('MRN')
mrncomp = mrncomp[mrncomp['have_count'] == 0]

mrncomp.to_csv(pandaData + "mrn_todo.csv", index=False)
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
                                        2:  'Robot'
                                        })
fullDocLog = fullDocLog.drop_duplicates(subset=['DocID'])   
#fullDocLog.to_csv(pandaData + "full_doc_log.csv")
'''