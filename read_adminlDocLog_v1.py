# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
pandaData = r'y:\Pandas_Data\\'

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
def parse_adminlog(line):
    
#08/13/2017 17:30:51 ROBOT8 9329 11_12_2015_Driver'sLicense_DocumentID_172901   
    pattern = r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2}) (ROBOT\d{1}) (\d{4}) (\d{2}_\d{2}_\d{4})_(.+)_DocumentID_(\d+)'
    m = re.match(pattern, line)
    if m != None:
        date = m[1]
        time = m[2]
        robot = m[3]
        MRN = m[4]
        docDate = m[5]
        docType = m[6]
        docID = m[7]
        fields = [date, time, robot, MRN, docDate, docType, docID]
    return fields
    
def read_adminlog(dir, robot):
    print ("Processing: " + robot)
    global allAdmin
    adminList = []
    fname = r'y:\Robot_Logs\\' + robot + 'adminDocs.txt'
    print("Processing: " + fname)
    with open(fname) as f:
        for line in f:
#           adminList = adminList + [line]
            row = parse_adminlog(line)
            adminList = adminList + [row]
#    print("outlistlen=" + str(len(adminList)) )
    clinicalDocDF = pd.DataFrame(adminList) 
    allAdmin = allAdmin.append(clinicalDocDF)
    return len(adminList)
#    return clinicalDocDF

dirname = r'y:\Robot_Logs\\'
allAdmin = pd.DataFrame()
robots = ['ROBOT0', 'ROBOT1', 'ROBOT2', 'ROBOT3',
          'ROBOT4', 'ROBOT5', 'ROBOT7', 'ROBOT8']
totcount = 0 
for robot in robots: 
    count = read_adminlog(dirname, robot)
    totcount = totcount + count
print ("Total Admin Docs=" + str(totcount))
allAdmin.to_csv(pandaData + "all_admin_docs.csv",index=False)
#allAdmin.to_csv(pandaData + "all_admin_docs.xlsx",index=False)


#allAdmin = allAdmin.rename(columns={3: 'MRN'})
'''
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
fullDocLog.to_csv(pandaData + "full_doc_log.csv")
08/13/2017 17:30:51 ROBOT8 9329 11_12_2015_Driver'sLicense_DocumentID_172901

'''