# -*- coding: utf-8 -*-

from time import gmtime, strftime
import pandas as pd
import numpy as np
import os
import time
import csv

def walk_files(directory_path):

    fname = open ('y:\\done_docs_WIP.csv', 'w')
    wr = csv.writer(fname, lineterminator='\n')

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
    fname.close()     
    tString1 =  str(docCount)
    print("Doc Count=" + tString1)


walk_files("x:\\Documents")

df = pd.read_csv('y:\\done_docs_WIP.csv')
print("done")
fileCount = df.groupby(['MRN']).count()['ExtID'].to_frame().rename(columns={'ExtID':'Count'})

print(fileCount.head())

file = 'y:\\test_BD.xlsx'
xl = pd.ExcelFile(file)
print (xl.sheet_names)
fullDocCount  = xl.parse('Sheet1')
fullDocCount['PID'] = fullDocCount['PID'].fillna(0)
fullDocCount['TEMP'] =  fullDocCount['PID'].astype('int')
fullDocCount['MRN'] =  "A" + fullDocCount['TEMP'].astype('str')
fullDoc = fullDocCount[['DocType','Count','MRN']]
totalDocCount = fullDoc['Count'].sum()
print("Total Doc Count")
print(totalDocCount)
docDelta = pd.merge(fileCount.reset_index(),fullDoc,on='MRN')
docDelta['delta'] = docDelta['Count_y'] - docDelta['Count_x']
       
print ("-----------------------------------")       
print(docDelta.head(10))

     
docDelta['newDelta']  = np.where(docDelta['delta'] < 0,0,docDelta['delta'] ) 
sorted = docDelta.sort_values(by='newDelta',ascending=False)
print(sorted.head(100))
thesum = docDelta['newDelta'].sum()
print(thesum)         

    