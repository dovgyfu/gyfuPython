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
p5 = write_df('Person_p5')
p6 = write_df('Person_p6')

nameSer = pd.DataFrame(nameList)
nameSer = nameSer.sort_values(1,0)
dataDict = nameSer.drop_duplicates(subset=1).reset_index()[[0,1]]
repDir = r'y:\MHNI_Data\gw_out\\'
dataDict.to_excel(repDir + "data_dict_xl.xlsx", index=False)
nameSer.to_csv(repDir + "data_dict.csv", index=False)
newMap  = dataDict[[1]].rename(columns={1: "origName"})
nameMap = pd.read_excel(repDir + 'data_dict_newmap.xlsx')[['origName', 'mapName']]
newCols = pd.merge(newMap, nameMap, how='outer', on='origName')
newCols.to_excel(repDir + "data_newdict.xlsx", index=False)

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
p5 = p5.rename(columns=ddict)
p6 = p6.rename(columns=ddict)

#keepp5 = p5.rename(columns=ddict)
m1 = pd.merge(p1, p2, how='outer', on='MRN', suffixes=["_p1", "_p2"])
m2 = pd.merge(m1, p3, how='outer', on='MRN', suffixes=['_m1', '_p3'])
m3 = pd.merge(m2, p4, how='outer', on='MRN', suffixes=['_m2', '_p4'])
m4 = pd.merge(m3, p5, how='outer', on='MRN', suffixes=['_m3', '_p5'])
m5 = pd.merge(m4, p6, how='outer', on='MRN', suffixes=['_m4', '_p6'])
allCols = m5.columns.to_series().sort_values().to_frame()
#cL = m5.columns
#cL = cL.to_series()
#print(type(cL))
#for i in cL:
#    print(i)

m5.to_excel(repDir + "merged_person.xlsx", index=False)    
#allCols = cL.sort_values().to_frame()
allCols['countall'] = 1
allCols = allCols.reset_index()[[0, 'countall']].rename(columns={0: 'name'})
allCols.to_csv(repDir + "colsFound.csv", index=False)

keepListDF = pd.read_csv(repDir + "newKeep.csv")
keepList = keepListDF[['MRN']].rename(columns={'MRN': 'name'})
keepList['countKeep'] = 1

mergeCols = pd.merge(allCols, keepList, how='outer', on='name')
keepList = keepList['name'].tolist()
#pd.read_csv(repDir + "keepList.csv")['MRN'].tolist()
colOrder = pd.read_excel(repDir + "colOrder.xlsx")
colOrder = colOrder['ColName'].tolist()

#keepListSer = pd.series(keepList)
patientdf = m5[colOrder]
patientdf = patientdf[patientdf['MRN'] != 'nan']
patientdf.to_csv(repDir + 'Patient_Demographics.csv', index=False)    
