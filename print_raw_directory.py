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

    fname = open ('y:\\done_fulldir.csv', 'w')
    wr = csv.writer(fname)

    docCount = 0
    
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)

           ftime = time.gmtime(created) 
           dspTime = strftime("%m/%d/%y,%H:%M,%S", ftime)
           allFields = [file_path, dspTime]
           docCount = docCount + 1
           wr.writerow(allFields)
    fname.close()     
    tString1 =  str(docCount)
    print("Doc Count=" + tString1)


walk_files("x:\\Documents")