# -*- coding: utf-8 -*-
"""
from time import gmtime, strftime
"""
from time import gmtime, strftime
import pandas as pd
import os
import time
import csv


file = 'y:\\full_chart_doc_count.xlsx'
xl = pd.ExcelFile(file)
print (xl.sheet_names)
fullDocCount  = xl.parse('Sheet1')
fullDocCount['PID'] = fullDocCount['PID'].fillna(0)
fullDocCount['TEMP'] =  fullDocCount['PID'].astype('int')
fullDocCount['MRN'] =  "A" + fullDocCount['TEMP'].astype('str')
fullDoc = fullDocCount[['DocType','Count','MRN']]

#fullDocCount['PID'].fillna[0]
#fullDocCount['MRN'] =  fullDocCount['PID'].astype('int')
#print (df1)
print(fullDoc.head())
docDelta = pd.merge(fileCount.reset_index(),fullDoc,on='MRN')
docDelta['delta'] = newShit['Count_y'] - newShit['Count_x']

