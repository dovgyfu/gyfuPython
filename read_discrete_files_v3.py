# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
import shutil
socList = []
vitalList = []
allergyList = []
problemList = []
familyList = []
surgicalList = []
pmhList = []
immuList = []
fname = r'y:\discrete_analysis.csv'
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

def process_Allergies(fname, fromDir, toDir):
    global allergyList
    print("Processing Allergies: " + fname)  
    allergyDir = toDir + "allergies\\"
    MRN = parse_MRN(fname)
    
    copyFile(fname, fromDir, allergyDir)
    file_path = allergyDir + fname
    df1 = pd.read_csv(file_path, skiprows=3, header=None)
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
        allergyList = allergyList + [row] 

def process_Family(fname, fromDir, toDir):

    global familyList
    print("Processing Family: " + fname)  
    fileDir = toDir + "family\\"
    MRN = parse_MRN(fname)
    
    copyFile(fname, fromDir, fileDir)
    file_path = fileDir + fname
    df1 = pd.read_csv(file_path, skiprows=3, header=None)
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
        familyList = familyList + [row] 
def process_PMH(fname, fromDir, toDir):
#    global row
#   global immuName
#    global df1
    global pmhList
    print("Processing PMH: " + fname)  
    fileDir = toDir + "pmh\\"
    MRN = parse_MRN(fname)
    
    copyFile(fname, fromDir, fileDir)
    file_path = fileDir + fname
    df1 = pd.read_csv(file_path, skiprows=3, header=None)
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
#        print(row)
#        print(immuName)
        pmhList = pmhList + [row] 

def process_Immunization(fname, fromDir, toDir):
#    global row
#   global immuName
#    global df1
    global immuList
    print("Processing Immunization: " + fname)  
    fileDir = toDir + "immunization\\"
    MRN = parse_MRN(fname)
    
    copyFile(fname, fromDir, fileDir)
    file_path = fileDir + fname
    df1 = pd.read_csv(file_path, skiprows=3, header=None)
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
        immuName = row[0]
#        print(row)
#        print(immuName)
        if immuName.startswith("Comments"):
            pass
        else:
            immuList = immuList + [row] 

def process_Surgical(fname, fromDir, toDir):

    global surgicalList
    print("Processing Surgical: " + fname)  
    fileDir = toDir + "surgical\\"
    MRN = parse_MRN(fname)
    
    copyFile(fname, fromDir, fileDir)
    file_path = fileDir + fname
    df1 = pd.read_csv(file_path, skiprows=3, header=None)
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
        surgicalList = surgicalList + [row] 


def process_Problems(fname, fromDir, toDir):
    global problemList
    print("Processing Problems: " + fname)  
    problemDir = toDir + "problems\\"
    MRN = parse_MRN(fname)
    
    copyFile(fname, fromDir, problemDir)
    file_path = problemDir + fname
    df1 = pd.read_csv(file_path, skiprows=1, header=None)
    for x in df1.index:
        row = [MRN] + df1.iloc[x].tolist() 
        problemList = problemList + [row] 

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
    global allDiscrete
    allDiscrete = []
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
        allDiscrete = allDiscrete + [allF]
        wr.writerow(allF)
                
        if fileName.startswith('social'):
            process_Social(fileName, fromDir, toDir)
#            break
        if fileName.startswith('vitals'):
            process_Vitals(fileName, fromDir, toDir)

        if fileName.startswith('problems'):
            process_Problems(fileName, fromDir, toDir)

        if fileName.startswith('allergies'):
            process_Allergies(fileName, fromDir, toDir)
        if fileName.startswith('surgical'):
            process_Surgical(fileName, fromDir, toDir) 
            
        if fileName.startswith('immunization'):
            process_Immunization(fileName, fromDir, toDir)
            
        if fileName.startswith('PMH'):
            process_PMH(fileName, fromDir, toDir)
        if fileName.startswith('family'):
            process_Family(fileName, fromDir, toDir)
        

    wrfname.close()     
#disDF = pd.DataFrame(allDiscrete)
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

allergyNames=["MRN",
            "allergyName",
            "allergyDate",
            "allergyReaction",
            "allergyNotes"]
allergyDF = pd.DataFrame(allergyList, columns=allergyNames)
allergyDF.to_csv(outDir + "allergy.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

problemNames={0: "MRN",
            1: "problemName",
            2: "problemOnsetDate",
            3: "problemNotes",
            4: "problemStatus"}

problemDF = pd.DataFrame(problemList)[[0, 1, 2, 3, 4]]
problemDF = problemDF.rename(columns=problemNames)
problemDF.to_csv(outDir + "problems.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

familyNames={0: "MRN",
            1: "famName",
            2: "famRelAge",
            3: "famNotes"}

familyDF = pd.DataFrame(familyList)[[0, 1, 2, 3]]
familyDF = familyDF.rename(columns=familyNames)
familyDF.to_csv(outDir + "family.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

surgicalNames={0: "MRN",
            1: "surgName",
            2: "surgDate",
            3: "surgNotes"}

surgicalDF = pd.DataFrame(surgicalList)[[0, 1, 2, 3]]
surgicalDF = surgicalDF.rename(columns=surgicalNames)
surgicalDF.to_csv(outDir + "surgical.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

immuNames={0: "MRN",
            1: "immuName",
            2: "immuMfg",
            3: "immuTradeName",
            4: "immuLotNumber",
            5: "immuRoute",
            6: "immuInjDate",
            7: "immuPubDate"}

immuneDF = pd.DataFrame(immuList)[[0, 1, 2, 3, 4, 5, 6, 7]]
immuneDF = immuneDF.rename(columns=immuNames)
immuneDF.to_csv(outDir + "immunizations.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

pmhNames={0: "MRN",
            1: "pmhName",
            2: "pmhDate",
            3: "pmhNotes"}

pmhDF = pd.DataFrame(pmhList)[[0, 1, 2, 3]]
pmhDF = pmhDF.rename(columns=pmhNames)
pmhDF.to_csv(outDir + "past_medical.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

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