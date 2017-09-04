# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
import shutil
socList = []
vitalList = []
fname = r'y:\discrete_analysis.csv'
def copyFile(fname, fromDir, toDir):
    print("copy file: " + fname + " from: " + fromDir + " To: " + toDir)
    if os.path.isdir(toDir):
        pass
    else:
        print("Making Dir: " + toDir)
        os.mkdir(toDir)
    ckFile = toDir + fname
    if os.path.isfile(ckFile):
        print("File: " +  ckFile + " exists - not copying")
    else:
        shutil.copy2(fromDir + fname, toDir)
def parse_MRN(fname):
    m = re.match(r'(\w+)_(\d{4})\.csv', fname)
    if m == None:
        print("ERROR - bad file name: " + fname)
        return
    MRN = m[2]
    return MRN
    
def process_Social(fname, fromDir, toDir):
    global socList     
    print("Processing SocialHistory: " + fname) 
    MRN = parse_MRN(fname)

    socialDir =  toDir + "SocialHistory\\"
    copyFile(fname, fromDir, socialDir)
    
    file_path = socialDir + fname
    df1 = pd.read_csv(file_path, skiprows=3, header=None, names=["socFinding",
                                                    "socStatus",
                                                    "socAge",
                                                    "socAmount",
                                                    "socNotes"])
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
        socList = socList + [row] 
        
def process_Vitals(fname, fromDir, toDir):
    global vitalList
    print("Processing Vitals: " + fname)  
    vitalsDir = toDir + "vitals\\"
    MRN = parse_MRN(fname)
    
    copyFile(fname, fromDir, vitalsDir)
    file_path = vitalsDir + fname
    df1 = pd.read_csv(file_path, skiprows=3, header=None, names=["vitalsDate",
                                                    "vitalsBP",
                                                    "vitalsPosition",
                                                    "vitalsHR",
                                                    "vitalsRR",
                                                    "vitalsTemp",
                                                    "vitalsWeight",
                                                    "vitalsHeight",
                                                    "vitalsO2",
                                                    "vitals"])
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
        vitalList = vitalList + [row] 

def read_dir_to_csv(fname):
    wrfname = open (fname, 'w')
    wr = csv.writer(wrfname,  lineterminator='\n')
    header = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    wr.writerow(header)
    fromDir = r'y:\Lopez_Discrete\\'
    toDir = r'y:\MHNI_Data\Discrete\\'
    socialDir = 'SocialHistory\\'
    vitalsDir = 'Vitals\\'

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
        if fileName.startswith('social'):
            process_Social(fileName, fromDir, toDir)
#            break
        if fileName.startswith('vitals'):
            process_Vitals(fileName, fromDir, toDir)

    wrfname.close()     

fname = r'y:\discrete_analysis_v2.csv'
outfname = r'y:\out_discrete.csv'

read_dir_to_csv(fname)

colNames=["MRN",
          "socFinding",
          "socStatus",
          "socAge",
          "socAmount",
          "socNotes"]
        
socialDF = pd.DataFrame(socList, columns=colNames)
outDir = r'y:\MHNI_Data\Discrete\\'
socialDF.to_csv(outDir + "SocialHistory.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

vitalNames=["MRN",
            "vitalsDate",
            "vitalsBP",
            "vitalsPosition",
            "vitalsHR",
            "vitalsRR",
            "vitalsTemp",
            "vitalsWeight",
            "vitalsHeight",
            "vitalsO2",
            "vitalsHC"]
vitalDF = pd.DataFrame(vitalList, columns=vitalNames)
vitalDF.to_csv(outDir + "Vitals.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

'''
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
'''