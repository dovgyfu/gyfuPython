
# -*- coding: utf-8 -*-

from time import gmtime, strftime
import pandas as pd
import numpy as np
import os
import time
import csv

def walk_files(directory_path, fname):

    wrfname = open (fname, 'w')
    wr = csv.writer(wrfname,  lineterminator='\n')

    docCount = 0
    header = ["ExtID", "DocID", "MRN", "DocDate", "DocType", "ExtDate", "extTime", "ftype", "dup", "File"]
    wr.writerow(header)
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)

           ftime = time.gmtime(created) 
           dspTime = strftime("%m/%d/%y,%H:%M:%S", ftime)
           
           if (filename.startswith("MHNI") or filename.startswith("Doc ID")) and filename.endswith(".pdf") :
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
                   docID = ["A" + docFields[1]]
                   mrn = ["A" + docFields[2]]
                   docDate = [docFields[3] + "/" + docFields[4] + "/" + docFields[5]] 
                   timeFields = dspTime.split(",")
                   allFields = docFields[:1]  + docID + mrn + docDate + docType + docFields[7:] + timeFields + fType + dupFile + fileArray
                   docCount = docCount + 1
#                   if mrn == "A1443":
                   wr.writerow(allFields)
    wrfname.close()     
    tString1 =  str(docCount)
    print("Doc Count=" + tString1)

print("===== Scanning the Documents Directory")
dataDir = r'y:\Pandas_Data\\'
docDir = r'x:\Documents'
fnameDocs = dataDir +  r'\00_Done_Docs.csv'
walk_files(docDir, fnameDocs)

print("Reading CSV of Doc List")
df = pd.read_csv(fnameDocs)
df  = df [(df['ftype'] == 'GOOD') & (df['dup'] == "NODUP" ) & (df['ExtID'] == "MHNI")]
numwDups = len(df)
df = df.drop_duplicates(['DocID', 'MRN', 'DocDate', 'DocType'])
numNDups = len(df)

doneDocList = df
doneDocList['MRN'] = doneDocList.MRN.str[1:]
doneDocList['DocID'] = doneDocList.DocID.str[1:]
doneDocList['done_count'] = 1
doneDocList.to_csv(dataDir + "doneDocList.csv")
print ("With DUps=" + str(numwDups) + " NumNDups=" + str(numNDups))

fileCount = df.groupby(['MRN']).count()['DocDate'].to_frame().rename(columns={'DocDate':'Count'})
fileCount = fileCount.reset_index()
totFiles = fileCount['Count'].sum()
print("Total Files Extracted: " + str(totFiles))
