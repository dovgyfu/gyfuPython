
# -*- coding: utf-8 -*-

from time import gmtime, strftime
import pandas as pd
import numpy as np
import os
import time
import csv
import re
import shutil
pandaData = r'y:\Pandas_Data\\'
docDir = r'x:\Documents\\'
junkDir = r'x:\Discarded_Misc\\'
dupDir = r'x:\Dup_Docs\\'
extraDir = r'x:\Extra_Docs\\'
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
def docCategory(ExtID):
    if ExtID == "MHNI":
        return "Clinical"
    elif ExtID == "AMHNI":
        return "Admin"
    else:
        return None
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
def moveFile(fname, fromDir, toDir):
    print("Move file: " + fname + " from: " + fromDir + " To: " + toDir)
    if os.path.isdir(toDir):
        pass
    else:
        print("Making Dir: " + toDir)
        os.mkdir(toDir)
    ckFile = toDir + fname
    if os.path.isfile(ckFile):
        pass
        print("File: " +  ckFile + " exists - not moving")
    else:
        print("MOVING File: " +  ckFile )

        shutil.move(fromDir + fname, toDir)
def walk_files(directory_path, fname):

    wrfname = open (fname, 'w')
    wr = csv.writer(wrfname,  lineterminator='\n')

    docCount = 0
    header = ["ExtID", "DocID", "MRN", "DocDate", "DocType", "DocCapDate", "DocCapTime", "ftype", "dup", "File"]
    wr.writerow(header)
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '/' + filename
           created     = os.path.getctime(file_path)

           ftime = time.gmtime(created) 
           dspTime = strftime("%m/%d/%y,%H:%M:%S", ftime)
           timeFields = dspTime.split(",")           
#           if (filename.startswith("MHNI") or filename.startswith("Doc ID")) and filename.endswith(".pdf") :
           keepFile = False
           if filename.startswith("MHNI")  and filename.endswith(".pdf") :
               fileArray = [filename]
               if filename.startswith("Doc ID"): 
                   filename = filename.replace("Doc ID", "DocID_")
               docFields = filename.split('_')
               docType = [docFields[-1].split(".")[0]]
               fType = ["GOOD"]
               dupFile = ["NODUP"]
               if docType[0].isdigit():
                   fType = ["BADFILE"]                   
               if '(' in docType[0]:
                   dupFile = ["DUP"]
               if len(docFields) > 5:
                   tmpDocID = docFields[1]
                   docID = ["A" + docFields[1]]
                   mrn = ["A" + docFields[2]]
                   docDate = [docFields[3] + "/" + docFields[4] + "/" + docFields[5]] 
                   allFields = docFields[:1]  + docID + mrn + docDate + docType + docFields[7:] + timeFields + fType + dupFile + fileArray
                   docCount = docCount + 1
#                   if mrn == "A1443":
                   if tmpDocID == '':
                       pass
                   else:
                       keepFile = True
                       wr.writerow(allFields)
           elif filename.startswith("AMHNI"):
               pattern = r'^(AMHNI)_(\d+)_(\d{4}).*_(\d{2}_\d{2}_\d{4})_(.+)\.pdf'
               m = re.match(pattern,filename)
               if m!= None:
                   extID, docID, mrn, docDate, docType = m.groups()
                   allFields = [extID, docID, mrn, docDate, docType] + timeFields + ['GOOD', 'NODUP', filename] 
                   docCount = docCount + 1
                   keepFile = True
                   wr.writerow(allFields)     
           if keepFile == False:
#               print("Bad File=" + filename)
               moveFile(filename, docDir, junkDir)
#                AMHNI_143561_8925_09_25_2014_Insurance Card

    wrfname.close()     
    tString1 =  str(docCount)
    print("Doc Count=" + tString1)
def countAdmin(extID):
    if extID.startswith('AMHNI'):
        return 1
    else:
        return 0

def countClinical(extID):
    if extID.startswith('AMHNI'):
        return 0
    else:
        return 1
def cleanDocID(DocID):
    if DocID.startswith("A"):
        return DocID[1:]
    else:
        return DocID

    
extradocs = pd.read_csv(pandaData + "extradocs.csv", dtype=object)
extrafiles = extradocs['File']
for file in dupFiles:
    moveFile(file, docDir, extraDir)
