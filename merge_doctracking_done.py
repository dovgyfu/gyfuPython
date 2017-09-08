
# -*- coding: utf-8 -*-

from time import gmtime, strftime
from datetime import datetime
import pandas as pd
import numpy as np
import os
import time
import csv
import re
pandaData = r'y:\Pandas_Data\\'
docDir = r'x:\Documents'
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

def docCategory(ExtID):
    if ExtID == "MHNI":
        return "Clinical"
    elif ExtID == "AMHNI":
        return "Admin"
    else:
        return None
def walk_files(directory_path, fname):

    wrfname = open (fname, 'w')
    wr = csv.writer(wrfname,  lineterminator='\n')

    docCount = 0
    header = ["ExtID", "DocID", "MRN", "DocDate", "DocType", "DocCapDate", "DocCapTime", "ftype", "dup", "File"]
    wr.writerow(header)
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)

           ftime = time.gmtime(created) 
           dspTime = strftime("%m/%d/%y,%H:%M:%S", ftime)
           timeFields = dspTime.split(",")           
#           if (filename.startswith("MHNI") or filename.startswith("Doc ID")) and filename.endswith(".pdf") :
           if filename.startswith("MHNI")  and filename.endswith(".pdf") :
               fileArray = [filename]
               if filename.startswith("Doc ID"): 
                   filename = filename.replace("Doc ID", "DocID_")
               docFields = filename.split('_')
               docType = [docFields[-1].split(".")[0]]
               fType = ["GOOD"]
               dupFile = ["NODUP"]
               if docType[0].isdigit():
                   fType = ["BADFILE"]                   
               if '(' in docType[0]:
                   dupFile = ["DUP"]
               if len(docFields) > 5:
                   tmpDocID = docFields[1]
                   docID = ["A" + docFields[1]]
                   mrn = ["A" + docFields[2]]
                   docDate = [docFields[3] + "/" + docFields[4] + "/" + docFields[5]] 
                   allFields = docFields[:1]  + docID + mrn + docDate + docType + docFields[7:] + timeFields + fType + dupFile + fileArray
                   docCount = docCount + 1
#                   if mrn == "A1443":
                   if tmpDocID == '':
                       pass
                   else:
                       wr.writerow(allFields)
           elif filename.startswith("AMHNI"):
               pattern = r'^(AMHNI)_(\d+)_(\d{4}).*_(\d{2}_\d{2}_\d{4})_(.+)\.pdf'
               m = re.match(pattern,filename)
               if m!= None:
                   extID, docID, mrn, docDate, docType = m.groups()
                   allFields = [extID, docID, mrn, docDate, docType] + timeFields + ['GOOD', 'NODUP', filename] 
                   docCount = docCount + 1
                   wr.writerow(allFields)                      
#                AMHNI_143561_8925_09_25_2014_Insurance Card

    wrfname.close()     
    tString1 =  str(docCount)
    print("Doc Count=" + tString1)
def countAdmin(extID):
    if extID.startswith('AMHNI'):
        return 1
    else:
        return 0

def countClinical(extID):
    if extID.startswith('AMHNI'):
        return 0
    else:
        return 1
def cleanDocID(DocID):
    if DocID.startswith("A"):
        return DocID[1:]
    else:
        return DocID

def scanDocs():    
    print("===== Scanning the Documents Directory")
    dataDir = r'y:\Pandas_Data\\'
    docDir = r'x:\Documents'
    fnameDocs = dataDir +  r'\00_Done_Docs.csv'
    walk_files(docDir, fnameDocs)
    
    print("Reading CSV of Doc List")
    df = pd.read_csv(fnameDocs)
    df  = df [(df['ftype'] == 'GOOD') & (df['dup'] == "NODUP" ) ]
    numwDups = len(df)
    df = df.drop_duplicates(['DocID', 'MRN', 'DocDate', 'DocType'])
    numNDups = len(df)
    
    doneDocList = df
    #doneDocList['MRN'] = doneDocList.MRN.str[1:]
    #doneDocList['DocID'] = doneDocList.DocID.str[1:]
    doneDocList['done_count'] = 1
    doneDocList['done_admin_count'] = doneDocList['ExtID'].map(countAdmin)
    doneDocList['done_clinical_count'] = doneDocList['ExtID'].map(countClinical)
    doneDocList['DocCategory'] = doneDocList.ExtID.map(docCategory)
    doneDocList.drop(['ExtID', 'ftype', 'dup'], axis=1, inplace=True)
    #doneDocList = doneDocList[(doneDocList['admin_count'] == 1) | (doneDocList['clinical_count'] == 1)]
    total_clinical = doneDocList['done_clinical_count'].sum()
    total_admin = doneDocList['done_admin_count'].sum()
    total_done = doneDocList['done_count'].sum()
    
    #doneDocList.loc['Total'] = pd.Series(doneDocList['done_clinical_count'].sum(), index=['admin_count'])
    #doneDocList.loc['Total'] = pd.Series(doneDocList['done_count'].sum(), index=['admin_count'])
    #doneDocList.loc['Total'] = pd.Series(doneDocList['done_admin_count'].sum(),
    #               index=['admin_count'])
    
    print('Total  Docs=' + str(total_done))
    print('Total Clinical Docs=' + str(total_clinical))
    print('Total Admin Docs=' + str(total_admin))
    
    doneDocList.to_csv(dataDir + "doneDocList.csv", index=False)
def cleanType(doctype):
    return doctype.strip()

fullDocStatus = pd.read_csv(pandaData + "FullDocStatusNoDup_new3.csv", dtype={'MRN': 'object',
                                                                              'DocID': 'object'})
fullDocStatus['DocModDTTM'] = fullDocStatus.DocModDate.map(valDate2)
fullDone = fullDocStatus[fullDocStatus['done_count'] == 1]
cleanDocReport = pd.read_csv(pandaData + "gw_doctracking.csv", dtype={'MRN': 'object', 'DocType': 'object'})
cleanDocReport['DocModDTTM'] = cleanDocReport.docModDate.map(valDate2)
docStatus = fullDocStatus[['DocID', 'DocType_x', 'MRN', 'DocModDTTM',
                           'DocCategory_x',  'done_count'
                           ]]
docStatus = docStatus.rename(columns={'DocType_x': 'DocType', 'DocCategory_x': 'DocCategory'})
docStatus = docStatus[docStatus['DocCategory'] == "Clinical"]
#docStatus['DocType'] = docStatus.DocType.map(cleanType)
cleanDocReport = cleanDocReport.fillna("")
cleanDocReport['DocType'] = cleanDocReport.DocType.map(cleanType)

cdt =cleanDocReport['DocType'].value_counts()
cdtdf = pd.DataFrame(cdt)
cdtdf = cdtdf.reset_index().rename(columns={'DocType': 'Freq'})
cdtdf = cdtdf.rename(columns={'index': 'DocType'})

cdtdf = cdtdf.sort_values('DocType')

docStatus.DocType = docStatus.DocType.fillna("aaaaNoDocType")
docStatus['DocType'] = docStatus.DocType.map(cleanType)

dst = docStatus['DocType'].value_counts()
dstdf = pd.DataFrame(dst)
dstdf = dstdf.reset_index().rename(columns={'DocType': 'Freq'})
dstdf = dstdf.rename(columns={'index': 'DocType'})

dstdf = dstdf.sort_values('DocType')

totdtyp = dstdf['Freq'].sum()
totctyp = cdtdf['Freq'].sum()
print ("totdtyp=" + str(totdtyp))
print ("totctyp=" + str(totctyp))
cdr = cleanDocReport[['MRN', 'DocType', 'DocModDTTM']]
cdr['report_count'] = 1
sumDocStatus = docStatus.groupby(['MRN', 'DocType', 'DocModDTTM']).sum().reset_index()
sumDocReport = cdr.groupby(['MRN', 'DocType', 'DocModDTTM']).sum().reset_index()
D7353 =sumDocReport[sumDocReport['MRN'] == '7353'].sort_values(['MRN', 'DocType', 'DocModDTTM'])
S7353 =sumDocStatus[sumDocStatus['MRN'] == '7353'].sort_values(['MRN', 'DocType', 'DocModDTTM'])

srtD7353 = D7353.sort_values(['MRN', 'DocType', 'DocModDTTM'])
srtS7353 = S7353.sort_values(['MRN', 'DocType', 'DocModDTTM'])

compData  = pd.merge(sumDocReport, sumDocStatus, how='outer', on=['MRN', 'DocType', 'DocModDTTM'])
'''
del allLog
del dupDocID
del fdl
del tsum

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

print ("With DUps=" + str(numwDups) + " NumNDups=" + str(numNDups))

fileCount = df.groupby(['MRN']).count()['DocDate'].to_frame().rename(columns={'DocDate':'Count'})
fileCount = fileCount.reset_index()
doneMRN = fileCount
doneMRN.to_excel(dataDir + "ROBOTX_chart_cfg.xlsx", index=False)
totFiles = fileCount['Count'].sum()
print("Total Files Extracted: " + str(totFiles))
print("Total Files Extracted: " + str(totFiles))
'''