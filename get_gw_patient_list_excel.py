# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
def valDate(date): 
#        return str(date)
#        print("Validating Date: " + date)
        try:
#            print(date)
            dtGood = True
            docDate = datetime.strptime(date, '%m/%d/%Y')
        except:
            dtGood=False

        if dtGood == True:
#            print(docDate)
            return docDate
        else:
            return None

def get_cols(fname):
    print("reading:=============================================" + file_path)

    df1 = pd.read_excel(file_path, sheetname='Sheet1', index=False)

    for col in df1.columns:
        print(col)
def get_df(fname):
    print("reading:=============================================" + file_path)

    df1 = pd.read_excel(file_path, sheetname='Sheet1', index=False)
    return df1 
  
repDir = r'y:\MHNI_Data\GW_Reports'
f1 = '\person_all_c.xls'
file_path = repDir + f1    
get_cols(file_path)    

f1 = '\Patient_Visit.xls'
file_path = repDir + f1
visitDF = get_df(file_path)
csvOut = repDir + r'\visit_out.csv'
#visitDF.to_csv(csvOut) 
file_path = csvOut
visits = pd.read_csv(file_path, dtype={0: 'str'} )
visits['VisitDate'] = visits['VisitDate'].map(valDate) 
print(visits.head(10))
