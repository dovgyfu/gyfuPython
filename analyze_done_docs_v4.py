
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
fnameDocs = r'y:\00_Done_Docs.csv'
walk_files("x:\\Documents", fnameDocs)

print("Reading CSV of Doc List")
df = pd.read_csv(fnameDocs)
df  = df [(df['ftype'] == 'GOOD') & (df['dup'] == "NODUP" ) & (df['ExtID'] == "MHNI")]

df.drop_duplicates(['DocID', 'MRN', 'DocDate', 'DocType'])

#cleandf = df['ftype'] where ftype = good and dup=nodup
fileCount = df.groupby(['MRN']).count()['DocDate'].to_frame().rename(columns={'DocDate':'Count'})
#print(fileCount)

totFiles = fileCount['Count'].sum()
print("================== TOT FILES================")
print(totFiles)

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
print("Total Doc Count")
print(docCount)
fileCount = fileCount.reset_index()
#print(temp1.head(5))
docDelta = pd.merge(fileCount, fullDoc, how='outer', on='MRN')

print("Number of merged rows=" + str(len(docDelta)))

docDelta = docDelta.rename(columns={'Count_y': 'totCount', 'Count_x': 'haveCount'})
#print(docDelta.head())
docDelta['haveCount'] = docDelta['haveCount'].fillna(0)
docDelta['delta'] = docDelta['totCount'] - docDelta['haveCount']
       
print ("-----------------------------------")       
#print(docDelta.head(10))

docDelta['newDelta']  = np.where(docDelta['delta'] < 0,0,docDelta['delta'] ) 

print(docDelta.head())
deltaSorted = docDelta.sort_values(by='newDelta',ascending=False)
#print(sorted.head(10))

deltaSorted.to_csv(r'y:\00_not_done.csv')

thesum = docDelta['newDelta'].sum()
print(thesum)         

    