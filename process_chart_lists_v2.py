
# -*- coding: utf-8 -*-

from time import gmtime, strftime
import pandas as pd
import numpy as np
import os
import time
import csv
from pandas import ExcelFile

def walk_files(directory_path, fname):

#    wrfname = open (fname, 'w')
#    wr = csv.writer(wrfname,  lineterminator='\n')

#    docCount = 0
#    header = ["ExtID", "DocID", "MRN", "DocDate", "DocType", "ExtDate", "extTime", "ftype", "dup", "File"]
#    wr.writerow(header)
    cldf = pd.DataFrame()
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)

 #          ftime = time.gmtime(created) 
 #          dspTime = strftime("%m/%d/%y,%H:%M:%S", ftime)
           
           chartList = pd.DataFrame()
#           print(chartList)
           if (filename.startswith("ROBOT")  and filename.endswith("chart_list.xlsx")):
#                   print(chartList)
#                   print(root)
#                   print(filename)
                   df1 = pd.read_excel(file_path, sheetname='chart_list', dtype={0 : 'str', 2: 'str'}, header=None)
                   status = pd.read_excel(file_path, sheetname='status',  header=None)
#                   print(status)
                   lastProcRow = status.iloc[0][1] + 1  
                   chartList = df1[[0, 1, 2, 19]]
                   clnull = chartList[0] != 'nan'
#                   print(clnull.head())
                   chartList = chartList[clnull]
#                   print(chartList.head(10))
#                   chartList.dropna(subset=[0], how='all', inplace=True)
 #                  print(chartList)
                   robotID = filename[0:6]
                   chartList['ROBOT'] = robotID
                   chartList[1] = chartList[1].fillna(0)
                   chartList[1] = chartList[1].astype('int')
                   chartList[19] = chartList[19].fillna("")
                   print(robotID + " lastprocRow=" + str(lastProcRow) + " TOT Rows=" + str(len(chartList)))
                   cldf = cldf.append(chartList)
#                   print (chartList.head())
    print(cldf.shape)
    return cldf

#                   wr.writerow(allFields)
#    wrfname.close()     

print("===== Scanning the Documents Directory")
fnameDocs = r'y:\Robot\robot_assign.csv'
#chartList = pd.DataFrame()
listDir = r'y:\Robot'
chartList = walk_files(listDir, fnameDocs)
chartList = chartList.reset_index()
#print(chartList)
file_path = listDir + r"\ROBOT0_chart_list.xlsx"
status = pd.read_excel(file_path, sheetname='status',  header=None)
lastProcRow = status.iloc[0][1]
print(lastProcRow)
                        

