# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
pandaData = r'x:\GYFU\Robot_Logs\\'


pattern2 = r'^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2} gyfyvm1\W+(\d+)\W+(\w+)\W+(\w+)'

pattern1 = r'^\d{2}\/\d{2}\/\d{4} '
p3 = r'^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2} gyfyvm1\W+(\d+)\W+(\w+)\W+(\w+)'
p4 = r'gyfyvm1\W+(\d{5,7})\W+(\w+)\W+(\w+)'
p5 = r'gyfyvm1.+?(\d{4,})\W+(\w+)\W+(\w+)'
p6 = r'\D*?(\d{4,})\W+(\w+)\W+(\w+)'

mrnlist = []
with open(pandaData + 'chartlist.txt') as f:
    for line in f:
        m = re.search(p5, line)
        if m:
#            print(line)
            t1 = m[1]
            t2 = m[2]
            t3 = m[3]
            mrnlist = mrnlist + [[t1, t2, t3, line]]
#            print("-------------" + t1)
            print(t1)
        else:
            m = re.search(p6, line)
            if m:
                m1 = m[1]
                m2 = m[2]
                m3 = m[3]
#                print(m1 + "---" + line)
                mrnlist = mrnlist + [[m1, m2, m3, line]]
                print(m1)
            pass
#            print("-------------" + line)
mrnDF = pd.DataFrame(mrnlist)
mrnDF = mrnDF.drop(3, axis=1)
mrnDF = mrnDF.sort_values(0)
mrnDF = mrnDF.drop_duplicates(subset=0)
mrnDF.to_csv(pandaData + "mrnList.csv", index=False)
