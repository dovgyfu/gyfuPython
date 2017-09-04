# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
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

def walk_files(directory_path):
    # Walk through files in directory_path, including subdirectories
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)
 #          modified    = os.path.getmtime(file_path)

            # Process stuff for the file here, for example...
 #          print ("%(fp)s %(cdttm)s" % {"fp": file_path, "cdttm": time.ctime(created)} )
           print ("%(fp)-70s \t %(cdttm)s" % {"fp": file_path, "cdttm": time.ctime(created)} )

 #          print ("    Created:       %s" % time.ctime(created))
 #          print ("    Last modified: %s" % time.ctime(modified))

# print "Or like this: " ,datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
walk_files("x:\\Documents")