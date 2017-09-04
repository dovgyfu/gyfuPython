# -*- coding: utf-8 -*-
"""
from time import gmtime, strftime
"""
from time import gmtime, strftime
import pandas as pd
import os
file = 'y:\\ROBOT0_chart_list.xlsx'
xl = pd.ExcelFile(file)
print (xl.sheet_names)
df1 = xl.parse('chart_list')
#print (df1)


t1 = os.stat(file)
print ("=======================================")
#print (t1)

import os
import time
import csv

def walk_files(directory_path):

    fname = open ('y:\\done_docs_WIP.csv', 'w')
    wr = csv.writer(fname, lineterminator='\n')

    docCount = 0
    header = ["ExtID", "DocID", "MRN", "DocDate", "DocType", "ExtDate", "extTime"]
    wr.writerow(header)
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)

           ftime = time.gmtime(created) 
           dspTime = strftime("%m/%d/%y,%H:%M:%S", ftime)
           
           if (filename.startswith("MHNI") or filename.startswith("Doc ID")) and filename.endswith(".pdf") :
               if filename.startswith("Doc ID"): 
                   filename = filename.replace("Doc ID", "DocID_")
               docFields = filename.split('_')
               docType = [docFields[-1].split(".")[0]]
               if docType[0].isdigit() or '(' in docType[0]:
                   continue
               if len(docFields) > 5:
                   docDate = [docFields[3] + "/" + docFields[4] + "/" + docFields[5]] 
                   timeFields = dspTime.split(",")
                   allFields = docFields[:3]  + docDate + docType + docFields[7:] + timeFields
                   docCount = docCount + 1
                   wr.writerow(allFields)
    fname.close()     
    tString1 =  str(docCount)
    print("Doc Count=" + tString1)


walk_files("x:\\Documents")
df = pd.read_csv('y:\\done_docs_WIP.csv')
print("done")