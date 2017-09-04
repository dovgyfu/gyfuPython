# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os

fname = r'y:\discrete_analysis.csv'

def read_dir_to_csv(fname):
    wrfname = open (fname, 'w')
    wr = csv.writer(wrfname,  lineterminator='\n')
    header = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    wr.writerow(header)

    dirName = r'y:\Lopez_Discrete'
    walkGen = os.walk(dirName)
    for Tuple in walkGen:
        print(type(Tuple))
    print(Tuple[0])
    fileList = Tuple[2]
    print(len(fileList))
    disDf = pd.DataFrame()
    df1 = pd.DataFrame()
    allF = []
    for fileName in fileList:
        fName =''
        extName = ''
        fL = []
    
        parseName = fileName.split(".")
        if len(parseName) == 2:
    #    if fileName.endswith(".csv"):
            fList = [fileName]
            fL = parseName[0].split("_")
            extName = parseName[1]
    #        allF = fList + [fName] + [extName] + fL
    #        df1 = df1.append([fL])
    #    else:
     #       pass
    #        df1 = df1.append([[fileName]])
        allF = [fileName] + parseName +  [fName]  + fL
    
        wr.writerow(allF)
    wrfname.close()     

fname = r'y:\discrete_analysis_v2.csv'
outfname = r'y:\out_discrete.csv'

read_dir_to_csv(fname)

x = pd.read_csv(fname)

f = open(fname)

csv_f = csv.reader(f)
wrfname = open (outfname, 'w')
wr = csv.writer(wrfname,  lineterminator='\n')
header = ["fileName", "Type", "MRN"]
wr.writerow(header)

for row in csv_f:
     csv = False
     if len(row) > 2:
         if row[2] == 'csv':
             csv = True
     if csv:
        fTest = row[1]
        m = re.match(r'(\w+)_(\d{4}$)', fTest)
        if m:
            fullM  = m[0]
            mtype = m[1]
            MRN = m[2]
            outrow = [fullM, mtype, MRN]
            wr.writerow(outrow)
            
            
wrfname.close()
dfx = pd.read_csv(outfname)         
#     for col in  row:
#             print (col + "," , end = " ")
#    print (row)