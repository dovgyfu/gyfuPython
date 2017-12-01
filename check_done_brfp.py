# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
import pandas as pd
import os
docList = []
def parseMRN(docdf, orownum, count):
               
                patient = ''
                docType = ''
 
                while count < 4:
                    rownum = orownum + count
                    row = docdf.iloc[[rownum]] 
                    patient = patient +  str(row.iat[0, 1])
                    docType = docType + str(row.iat[0, 2])
#                    print(docType)
#                    print(patient)
                    m = re.match(r"(.+)\[(\d+)\]", patient)
                    if m == None:
                        count = count + 1   
                        
                    else:
                        MRN = m[2]
                        pName = m[1]
                        return [pName, MRN, docType]
#                row = docdf.iloc[[rownum]] 
                print("BAD ROWNUM= " + str(rownum))
                print(row)
                return ["NO Patient", "NOMRN", "NODOC"]
                                    
def parseDocType(docdf, startrow, count):
    count = 0
    docType = ''
#    print ("In parse doc Type")
    newdf = docdf[startrow:startrow+5]
#    print(len(newdf))
#    print(newdf)
    row = newdf.loc[[startrow]]
    docType = docType + str(row.iat[0, 2])    
    rowsleft = len(newdf)
    
    while rowsleft > 2 :
#        print("DocType=" + docType)
        nextrow = newdf.loc[[startrow+count+1]]
 #       print(type(nextrow))
        nextdate = nextrow.iat[0,0]
#        print(type(nextdate))
#        print(nextdate)
        if type(nextdate) == float:
#            print("NEXTDATE is NAN")
            docType = docType + " " + str(nextrow.iat[0, 2])    
            count = count + 1
            rowsleft = rowsleft - 1
        else:
#            print("NETDATE is NOT NAN")
#            print("Completed DocType: " + docType)
            return docType
            break
    return docType
def valDate(date): 
#        return str(date)
#        print("Validating Date:" + date + ":")
        try:
 #           print(date)
            dtGood = True
            docDate = datetime.strptime(date, '%m/%d/%Y')
        except:
            dtGood=False

        if dtGood == True:
#            print(docDate)
            return docDate
        else:
#            print( date)
            return None

def walk_doc_lists(directory_path):
#    global df1
    cldf = pd.DataFrame()
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '\\' + filename
#           print(filename)
#           if (filename.startswith("gw_doctracking_2017_090717")  and filename.endswith(".xls")):

           if (filename.startswith("gw")  and filename.endswith(".xls")):
                   print("reading: " + file_path)
                   df1 = pd.read_excel(file_path, sheetname='Sheet1', header=None, index=False)
                   df1 = df1[14:]
                   df1 = df1[[0, 2, 8]]
                   df1 = df1.dropna(axis=0, how='all',subset=[2,8])
                   df1 = df1[df1[0] != "Note"]
                   df1 = df1[df1[0] != "Date"]
                   
#                   print(df1.head())
#docDelta = docDelta.rename(columns={'Count_y': 'totCount', 'Count_x': 'haveCount'})                   
                   cldf = cldf.append(df1)
    print(cldf.shape)
    return cldf


def ckDate(date):
    if type(date) == 'str':
        return "string"
    else:
        return "date"
def state_0(x):
    global docReport
    global xstate
    global noDateCount
    global goodDateCount
    global patient
    global docType
    global prevDate
    global docList
#    global row
#    print("--------------state =0 ---------------------------")
#   print(x)        
    DocDate = docReport.iat[x, 1]
    print(DocDate)
    

    pyDate = valDate(DocDate)
    if pyDate == None:   
        noDateCount = noDateCount + 1
    else:
        prevDate = pyDate
        goodDateCount = goodDateCount + 1
        xstate = 1
        patient = docReport.iat[x,2]
        docType = docReport.iat[x,3]

        print(patient + ":" + docType)
def state_1(x):
    global docReport
    global xstate
    global noDateCount
    global goodDateCount
    global patient
    global docType
    global prevDate
    global docList 
#    global row
#    row = docReport.iloc[[x]]
#    print("--------------state =1 ---------------------------")
        
#    row = row.fillna("NULL")
#    print(x)        
    DocDate = docReport.iat[x, 1]
#    print(DocDate)


    pyDate = valDate(DocDate)
    if pyDate == None:   
        noDateCount = noDateCount + 1
        patient = patient + " " + docReport.iat[x,2]
        docType = docType + " " + docReport.iat[x,3]

    else:
#        print(prevDate)
#        print(patient + ":" + docType)
        docList = docList + [[prevDate, patient, docType]]
        patient = docReport.iat[x,2]
        docType = docReport.iat[x,3]
        prevDate = pyDate

        goodDateCount = goodDateCount + 1
        xstate = 1


def process_raw_report(rawlist):
        global docReport
        global xstate
        global noDateCount
        global goodDateCount
        global patient
        global docType
        global docList
    
        docReport = rawlist.reset_index().fillna("")
        xstate = 0
        noDateCount = 0
        goodDateCount = 0
        patient = ""
        docType = ""
        for x in docReport.index:
#            print(x)       
            if xstate == 0:
                state_0(x)
            elif xstate == 1:
                state_1(x)
        docList = docList + [[prevDate, patient, docType]]
        docDF = pd.DataFrame(docList)              
            
            
#                print("Good Date=" + str(pyDate))
        print("Good Date Count =" + str(goodDateCount))
        print("Bad Date Count =" + str(noDateCount))
        return docDF

#            print(docDate)

def parse_MRN(patient):
    pattern = r'(.*) \[(\d{4})\]'
    m = re.match(pattern, patient)
    if m == None:
        return 'NoMRN'
    else:
        pName = m[1]
        MRN = m[2]
        return MRN

    return MRN 
def write_cfg(robot, list):
    global pandasData
    if len(list) > 0:
        xlFile =  gyfuDir + robot + "_cfg.xlsx"
        print(xlFile)
        df = pd.DataFrame(list)
#        df.to_excel(xlFile, sheet_name="chart_list", header=False)
        status= [["LastRow", -1, 0]]
        st = pd.DataFrame(status)
        xlwtr = pd.ExcelWriter(xlFile, engine='xlsxwriter')
        df.to_excel(xlwtr, sheet_name="chart_list", header=False,index=False)

        st.to_excel(xlwtr, sheet_name='status',header=False,index=False)
        xlwtr.save()
        xlwtr.close()
def write_csv_cfg(robot, list):
    global pandasData
    gyfuDir = r'x:\GYFU\Robot\\'
    if len(list) > 0:
        xlFile =  gyfuDir + robot + "_cfg.csv"
        print(xlFile)
        df = pd.DataFrame(list)
#        df.to_excel(xlFile, sheet_name="chart_list", header=False)
        status= [["LastRow", -1, 0]]
        df.to_csv(xlFile, header=False,index=False)

def walk_dir(directory_path):
#    global df1
    cldf = pd.DataFrame()
    fList = []
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '\\' + filename
#           print("reading: " + filename)
           p = r'P_(\d+).pdf'
           m = re.match(p, filename)
           if m:
               MRN = m[1]
               print("reading: " + filename + " MRN=" + MRN)

               fList = fList + [MRN]
                   
    return fList

brfp_dir = r'X:\GYFU\GYFU_rs1\MHDIBRFP\BRFP_batch1\\'       
brfp_dir = r'X:\GYFU\BRFP\\'       

listDir = r'y:\MHNI_Data\DocTracking\\' 
pandawork = r'y\Pandas_Work\\'
pandadata = r'y:\Pandas_Data\\'
gyfuDir = r'x:\GYFU\\'
gyfuDir = r'x:\GYFU\Robot\\'
doneList = walk_dir(brfp_dir)
doneDF = pd.DataFrame(doneList)
doneDF = doneDF.rename(columns={0: "MRN"})
fullList = pd.read_excel(gyfuDir + "sample_100.xlsx", dtype=object)

fullList = fullList.rename(columns={"Patient Number": "MRN"})
t = fullList['MRN']
y = t.str.strip()
ydf = pd.DataFrame(y)
fullList["fullCount"] = 1
doneDF["doneCount"] = 1


merge1 = pd.merge(ydf, doneDF, how="outer", on="MRN")      

docList = fullList
rList =  ['ROBOT0', 'ROBOT1', 'ROBOT2',
              'ROBOT3',
              'ROBOT4',
              'ROBOT5',
              'ROBOT7',
              'ROBOT8']
rIter = iter(rList)
numDocs = len(docList)
print(numDocs)
docsPerRobot = int(numDocs / 8)
cfgdf = []
i = 1
y = 1

for doc in docList.index:
    row = docList.loc[[doc]]
    print(doc)
    
    if i > docsPerRobot or y >= numDocs-1:
        i = 1
        try:
            robot = next(rIter)
            print(robot)
            write_csv_cfg(robot, cfgdf)
            cfgdf = []
        except:
            print (i)
    rowList = row.values.tolist()       
    cfgdf = cfgdf + rowList
    i = i + 1
    y = y + 1 
  
    
       



