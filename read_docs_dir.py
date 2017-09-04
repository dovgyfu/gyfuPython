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

    fname = open ('y:\\done_docs3.csv', 'w')
    wr = csv.writer(fname, lineterminator='\n')

    docCount = 0
    
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)

           ftime = time.gmtime(created) 
           dspTime = strftime("%m_%d_%y,%H:%M,%S", ftime)
           
           if (filename.startswith("MHNI") or filename.startswith("Doc ID")) and filename.endswith(".pdf") :
               if filename.startswith("Doc ID"): 
                   filename = filename.replace("Doc ID", "DocID_")
               docFields = filename.split('_')
               if len(docFields) > 5:
                   docDate = [docFields[3] + "_" + docFields[4] + "_" + docFields[5]] 
                   timeFields = dspTime.split(",")
                   allFields = docFields + docDate + timeFields
                   docCount = docCount + 1
                   wr.writerow(allFields)
    fname.close()     
    tString1 =  str(docCount)
    print("Doc Count=" + tString1)


walk_files("x:\\Documents")