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

fs = "Doc ID1234"
t2 = fs.replace("D", "B")
print(t2)
