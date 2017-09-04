# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
import shutil
outList = []
fname = r'y:\docList.csv'
def valDate(date): 
#        return str(date)
#        print("Validating Date: " + date)
        try:
#            print(date)
            dtGood = True
            docDate = datetime.strptime(date, '%m_%d_%Y %H_%M_%S')
        except:
            dtGood=False

        if dtGood == True:
#            print(docDate)
            return docDate
        else:
            return None
def read_doclist(fname, MRN, sheetname):
    global doclistdf
    
    file_path = fname
    print("Start reading:=============================================" + file_path)
    doclistdf = pd.read_excel(file_path, sheetname=sheetname, index=False, header=None)
    doclistdf = doclistdf.dropna(how='all')
    doclistdf['MRN'] = MRN
    
    return doclistdf

def get_df(fname, MRN):
    global df1
    global outList
    
    file_path = fname
#    print("Start reading:=============================================" + file_path)
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
    df1 = pd.read_excel(file_path, sheetname=None, index=False)
    sheetList = list(df1.keys())
#    newRow = [file_path] + sheetList
    if 'status' in sheetList:
        status = 'status'
    else:
        status = ''
    numSheets = len(sheetList)
    maxD = 0
    for sheet in sheetList:
        if sheet not in ['status', 'Sheet1']:
            doclist = read_doclist(file_path, MRN, sheet)
            docCount = len(doclist)
            if docCount > maxD:
                maxD = docCount
    newRow = [MRN] + [maxD] + [file_path] + [numSheets] + [status] + sheetList
    outList = outList + [newRow]              
    
    return df1 
def copyFile(fname, fromDir, toDir):
#    print("copy file: " + fname + " from: " + fromDir + " To: " + toDir)
    if os.path.isdir(toDir):
        pass
    else:
        print("Making Dir: " + toDir)
        os.mkdir(toDir)
    ckFile = toDir + fname
    if os.path.isfile(ckFile):
        pass
#        print("File: " +  ckFile + " exists - not copying")
    else:
        shutil.copy2(fromDir + fname, toDir)

def process_docFile(fileName, MRN):
    get_df(fileName, MRN)
    
#    print(fileName)

def read_excel_docList(inputDir, outFname):
    fname = outFname
    wrfname = open (fname, 'w')
    wr = csv.writer(wrfname,  lineterminator='\n')
    header = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    wr.writerow(header)

    walkGen = os.walk(inputDir)
    for Tuple in walkGen:
        pass
#        print(type(Tuple))
    print(Tuple[0])
    fileList = Tuple[2]
    print(len(fileList))
    disDf = pd.DataFrame()
    df1 = pd.DataFrame()
    allF = []
    global allDiscrete
    allDiscrete = []
    for fileName in fileList:
        fName =''
        extName = ''
        fL = []
    
        parseName = fileName.split(".")
        if len(parseName) == 2:
            fList = [fileName]
            fL = parseName[0].split("_")
            extName = parseName[1]
            MRN = fL[0]
            fType = fL[1]
        allF = [fileName] + parseName +  [MRN]  + [fType]
        allDiscrete = allDiscrete + [allF]
        if extName == 'xlsx':
            process_docFile(inputDir + fileName, MRN)
        wr.writerow(allF)
    wrfname.close()


dirName = r'y:\MHNI_Data\doclists\\'
'''
print("fname=" + fname)
read_excel_docList(dirName, fname)
outDF = pd.DataFrame(outList)
outDF.to_excel(dirName + "..\\" + "outdf.xlsx")

MRNSheets = []
for row in outDF.index:
        x = outDF.iloc[row]
        MRN = x[0]
        num = x[3]
        slist = x[4:4+num]
        for sheet in slist:
            if sheet not in ['Sheet1', 'status']:
                tmpRow = [MRN, num, sheet]
                MRNSheets = MRNSheets + [tmpRow]
MRNdf = pd.DataFrame(MRNSheets)
MRNdf[3] = MRNdf[2].map(valDate)
sortedMRN = MRNdf.sort_values([0, 3], ascending=[True, False])
print("Before Dedupe: " + str(len(sortedMRN)))
MRNdocList = sortedMRN.drop_duplicates(subset=0)
print("After Dedupe: " + str(len(MRNdocList)))
MRNdocList = MRNdocList.reset_index()
fdl = pd.DataFrame()

for row in MRNdocList.index:
#    print(row)
    MRN = MRNdocList.iat[row, 1]
    sheet = MRNdocList.iat[row, 3]
    fname = dirName + MRN + "_doclist.xlsx"
#    print(MRN)
    xldf = read_doclist(fname, MRN, sheet)
    fdl = fdl.append(xldf)
    

#                print(MRN + " " + str(num) + " " + sheet)
#        print(x)
'''
ChartsWithDocs = fdl.drop_duplicates(subset='MRN')[['MRN']]
ChartsWithDocs.to_csv(r'y:\chartswithDocs.csv',index=False)
