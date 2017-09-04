# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os


def ckDate(date):
    ftype = type(date)
    return len(date)
    if ftype == 'str':
        print("string")
        return ftype
    else:
        print(ftype)
        return ftype
    if type(date) == 'str':
        return "string"
        
    else:
        return "date"
def valDate(date): 
#        return str(date)
#        print("Validating Date: " + date)
        lend = len(date)
        if lend > 10:
            date = date[0:10]
        try:
#            print(date)
            dtGood = True
            docDate = datetime.strptime(date, '%Y-%m-%d')
        except:
            dtGood=False

        if dtGood == True:
#            print(docDate)
            return docDate
        else:
            return None    
def fixDoctype(DocType):
    if DocType.endswith('nan'):
        DocType = DocType[:-3]
    else:
        DocType = DocType
    return DocType
listDir = r'y:\MHNI_Data\\' 
pandawork = r'y:\Pandas_Work\\'
pandadata = r'y:\Pandas_Data\\'

gwreportdocs = pd.read_csv(pandadata + 'gw_doctracking.csv', dtype={'MRN': 'str'})

gwreportdocs['count'] = 1
grp = gwreportdocs.groupby(['MRN'])
mrnsumGW = grp.sum().reset_index()
mrnsumDone = fileCount

comp = pd.merge(mrnsumGW, mrnsumDone, how='outer', on='MRN').fillna(0)
comp['delta'] = comp['count'] - comp['Count']
goodm = comp[comp['delta'] == 0]

#comp['delta'] = comp['count_x'] - comp['count_y']





