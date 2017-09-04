
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
dataDir = r'y:\MHNI_Data'
docDir = r'x:\Documents'
chartFile = r'y:\\full_chart_doc_count.xlsx'
fnameDocs = dataDir +  r'\00_Done_Docs.csv'
walk_files(docDir, fnameDocs)

print("Reading CSV of Doc List")
df = pd.read_csv(fnameDocs)
df  = df [(df['ftype'] == 'GOOD') & (df['dup'] == "NODUP" ) & (df['ExtID'] == "MHNI")]

df.drop_duplicates(['DocID', 'MRN', 'DocDate', 'DocType'])

fileCount = df.groupby(['MRN']).count()['DocDate'].to_frame().rename(columns={'DocDate':'Count'})

totFiles = fileCount['Count'].sum()
print("Total Files Extracted: " + str(totFiles))

file = chartFile
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

fileCount = fileCount.reset_index()
#print(temp1.head(5))
docDelta = pd.merge(fileCount, fullDoc, how='outer', on='MRN')
print("Number of merged rows=" + str(len(docDelta)))

docDelta = docDelta.rename(columns={'Count_y': 'totCount', 'Count_x': 'haveCount'})
docDelta = docDelta.dropna(subset=['totCount'])
print("Number of merged rows after dropna=" + str(len(docDelta)))

#print(docDelta.head())
docDelta['haveCount'] = docDelta['haveCount'].fillna(0)
docDelta['delta'] = docDelta['totCount'] - docDelta['haveCount']
       
print ("-----------------------------------")       

docDelta['newDelta']  = np.where(docDelta['delta'] < 0,0,docDelta['delta'] ) 
deltaDF = docDelta
deltaDF.MRN = deltaDF.MRN.str[1:]
deltaDF.delta = deltaDF.delta.astype('int')
deltaDF.newDelta = deltaDF.newDelta.astype('int')

havenone = deltaDF['haveCount'] == 0
deltaNone = deltaDF[havenone]

deltaSorted = deltaNone.sort_values(by='newDelta',ascending=False)
deltaSorted.to_csv(r'y:\00_none_done.csv', index=False)

deltaDF = deltaDF.sort_values(by='newDelta',ascending=False)
deltaDF.to_csv(r'y:\00_full_status.csv', index=False)

noneSum = deltaNone['newDelta'].sum()
print("Number of Docs left from untouched accts: " + str(int(noneSum)) ) 
       
allSum = deltaDF['newDelta'].sum()
print("Number of Docs left Total: " + str(int(allSum)))  

    