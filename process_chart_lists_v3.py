
# -*- coding: utf-8 -*-

import pandas as pd
import os

def walk_files(directory_path, fname):

    cldf = pd.DataFrame()
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename

           
           chartList = pd.DataFrame()
           if (filename.startswith("ROBOT")  and filename.endswith("chart_list.xlsx")):
                   df1 = pd.read_excel(file_path, sheetname='chart_list', dtype={0 : 'str', 2: 'str'}, header=None)
                   status = pd.read_excel(file_path, sheetname='status',  header=None)
                   lastProcRow = status.iloc[0][1] + 1  
                   chartList = df1[[0, 1, 2, 19]]
                   clnull = chartList[0] != 'nan'
                   chartList = chartList[clnull]
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


print("===== Scanning the Documents Directory")
fnameDocs = r'y:\Robot\robot_assign.csv'

listDir = r'y:\Robot'
chartList = walk_files(listDir, fnameDocs)
chartList = chartList.reset_index()

file_path = listDir + r"\ROBOT0_chart_list.xlsx"
status = pd.read_excel(file_path, sheetname='status',  header=None)
lastProcRow = status.iloc[0][1]
print(lastProcRow)
                        

