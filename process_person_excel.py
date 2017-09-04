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
    file_path = fname
    print("reading:=============================================" + file_path)
    dtype = {0: 'str',
             1: 'str',
             2: 'str',
             3: 'str',
             4: 'str',
             5: 'str',
             6: 'str',
             7: 'str',
             8: 'str',
             9: 'str'
             }
    df1 = pd.read_excel(file_path, sheetname='Sheet1', index=False, dtype=dtype)

    return df1 
def write_df(fname) :
    global nameList 
    repDir = r'y:\MHNI_Data\gw_out\\'
    f1 = fname
    ext = '.xls'
    file_path = repDir + f1 + ext   
    print(file_path)
    p1 = get_df(file_path) 
    for col in p1.columns:
#        renstr = '"' + col + '":' + ' "news",'
        renstr = col
        nameList = nameList +  [[f1, renstr]]
#    print(renstr)
    
    file_path = repDir + f1 + "_out" + ".csv"
    p1.to_csv(file_path, index=False, sep=',',quoting=csv.QUOTE_NONNUMERIC) 
    return p1
nameList = []    
p1 = write_df('Person_p1')
p2 = write_df('Person_p2') 
p3 = write_df('Person_p3')
p4 = write_df('Person_p4')
#p5 = write_df('Person_p5')

nameSer = pd.DataFrame(nameList)
nameSer = nameSer.sort_values(1,0)
dataDict = nameSer.drop_duplicates(subset=1).reset_index()[[0,1]]
repDir = r'y:\MHNI_Data\gw_out\\'
dataDict.to_excel(repDir + "data_dict_xl.xlsx", index=False)
nameSer.to_csv(repDir + "data_dict.csv", index=False)
nameMap = pd.read_excel(repDir + 'data_dict_map.xlsx')[['origName', 'mapName']]
#nameMap = nameMap.set_index('origName')
ddict={}
for row in nameMap.index:
    oName = nameMap.at[row, "origName"]
    mName = nameMap.at[row, "mapName"]
    mName = mName.replace(" ","")
    ddict.update({oName: mName})
p1 = p1.rename(columns=ddict)
p2 = p2.rename(columns=ddict)
p3 = p3.rename(columns=ddict)
p4 = p4.rename(columns=ddict)
#keepp5 = p5.rename(columns=ddict)
m1 = pd.merge(p1, p2, how='outer', on='MRN', suffixes=["_p1", "_p2"])
m2 = pd.merge(m1, p3, how='outer', on='MRN', suffixes=['_m1', '_p3'])
m3 = pd.merge(m2, p4, how='outer', on='MRN', suffixes=['_m2', '_p4'])
cL = m3.columns.sort_values()
#for i in cL:
#    print(i)

m3.to_excel(repDir + "merged_person.xlsx", index=False)    
s = cL.to_series()
s.to_csv(repDir + "stoCSV.csv", index=False)

keepList = pd.read_csv(repDir + "keepList.csv")['MRN'].tolist()
patientdf = m3[keepList]
patientdf.to_csv(repDir + 'Patient_Demographics.csv', index=False)
    
#m4 = pd.merge(m3, p5, how='outer', on='MRN', suffixes=['_m3', '_p5'])

#print(ddict) 
   
#print (nameSer)
#write_df('Person_p2')
#write_df('Person_p3')
#write_df('Person_p4')
#write_df('Person_p5')

'''
f1 = '\Patient_Visit.xls'
file_path = repDir + f1
visitDF = get_df(file_path)
csvOut = repDir + r'\visit_out.csv'
#visitDF.to_csv(csvOut) 
file_path = csvOut
visits = pd.read_csv(file_path, dtype={0: 'str'} )
visits['VisitDate'] = visits['VisitDate'].map(valDate) 
print(visits.head(10))
'''