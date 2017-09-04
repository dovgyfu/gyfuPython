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
print (df1)


t1 = os.stat(file)
print ("=======================================")
print (t1)

import os
import time
import csv

with open ('y:\\done2_docs.csv', 'w') as fname:
    wr = csv.writer(fname, dialect='excel')
    filename = "test_1_234_567"
#docFields = filename.split('_')
    docFields = ['1', 'abc']
#timeFields = dspTime.split(",")
#    allFields = docFields + timeFields
 #              print(allFields)
    wr.writerow(docFields)
 #              for item in allFields:
 #                  print(item)
               
#               fname.write(allFields)

 #          print ("    Created:       %s" % time.ctime(created))
 #          print ("    Last modified: %s" % time.ctime(modified))

# print "Or like this: " ,datetime.datetime.now().strftime("%y-%m-%d-%H-%M")