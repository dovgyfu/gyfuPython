
# -*- coding: utf-8 -*-

from time import gmtime, strftime
import pandas as pd
import numpy as np
import os
import time
import csv
import re
import shutil
pandaData = r'y:\Pandas_Data\\'
docDir = r'x:\Documents\\'
junkDir = r'x:\Discarded_Misc\\'
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
def docCategory(ExtID):
    if ExtID == "MHNI":
        return "Clinical"
    elif ExtID == "AMHNI":
        return "Admin"
    else:
        return None
def copyFile(fname, fromDir, toDir):
#    print("copy file: " + fname + " from: " + fromDir + " To: " + toDir)
    if os.path.isdir(toDir):
        pass
    else:
        print("Making Dir: " + toDir)
        os.mkdir(toDir)
    ckFile = toDir + fname
    if os.path.isfile(ckFile):
        pass
#        print("File: " +  ckFile + " exists - not copying")
    else:
        shutil.copy2(fromDir + fname, toDir)
def moveFile(fname, fromDir, toDir):
    print("Move file: " + fname + " from: " + fromDir + " To: " + toDir)
    if os.path.isdir(toDir):
        pass
    else:
        print("Making Dir: " + toDir)
        os.mkdir(toDir)
    ckFile = toDir + fname
    if os.path.isfile(ckFile):
        pass
        print("File: " +  ckFile + " exists - not moving")
    else:
        shutil.move(fromDir + fname, toDir)
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
           keepFile = False
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
                       keepFile = True
                       wr.writerow(allFields)
           elif filename.startswith("AMHNI"):
               pattern = r'^(AMHNI)_(\d+)_(\d{4}).*_(\d{2}_\d{2}_\d{4})_(.+)\.pdf'
               m = re.match(pattern,filename)
               if m!= None:
                   extID, docID, mrn, docDate, docType = m.groups()
                   allFields = [extID, docID, mrn, docDate, docType] + timeFields + ['GOOD', 'NODUP', filename] 
                   docCount = docCount + 1
                   keepFile = True
                   wr.writerow(allFields)     
           if keepFile == False:
#               print("Bad File=" + filename)
               moveFile(filename, docDir, junkDir)
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

    
print("===== Scanning the Documents Directory")
dataDir = r'y:\Pandas_Data\\'
docDir = r'x:\Documents\\'
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

doneDocList = pd.read_csv(pandaData + "doneDocList.csv", dtype={'DocID': 'str'})
doneDocList['DocID'] = doneDocList.DocID.map(cleanDocID)
doneDocList['MRN'] = doneDocList.MRN.map(cleanDocID)

###################################################################################
#
# Get the full counts of admin and clinical and compare to what we have 
#
#####################################################################################

adminLog = pd.read_csv(pandaData + "all_admin_docs.csv", skiprows=1, header=None, names=['CapDate', 'CapTime', 
                                                                'Robot',
                                                                'MRN', 'DocCreateDate', 'DocType',
                                                                'DocID'],
                                                            dtype={'MRN': 'str',
                                                                   'DocID': 'str'})
adminLog['DocCategory'] = 'Admin'
adminLog['fdlCount'] = 1
adminLog['Signed'] = 'Signed'
adminLog['SignCount'] = 1


adminLog['docCreateDTTM'] = adminLog.DocCreateDate.map(valDate) 
fullDocLog = pd.read_csv(pandaData + "fullDocLog.csv", dtype={'DocID': 'str', 'MRN': 'str'})
fullDocLog = pd.concat([fullDocLog, adminLog])

fullDocStatus = pd.merge(fullDocLog, doneDocList, how='left', on=['DocID', 'MRN'])
fullDocStatus.drop(['Robot'], axis=1, inplace=True)

fullDocStatus.to_csv(pandaData + "FullDocStatus.csv", index=False)
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