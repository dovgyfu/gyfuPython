# -*- coding: utf-8 -*-
# version 4 
# version 5
# version 6 
import csv
import re
from datetime import datetime
import pandas as pd
import os
pandasData = r'y:\Pandas_Data\\'
pandasWork = r'y:\Pandas_Work\\' 
def parseMRN(docdf, orownum, count):
#                return    ["A", "B", "C"]          
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
#    return ["A", "B", "C"]
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

def read_docReport(file_path):

       cldf = pd.DataFrame()
       print("reading: " + file_path)
       df1 = pd.read_excel(file_path, sheetname='Sheet1', header=None, index=False)
       df1 = df1[14:]
       df1 = df1[[0, 2, 8, 9]]
       df1 = df1.dropna(axis=0, how='all')
       '''
       df1 = df1[df1[0] != "Note"]
       df1 = df1[df1[0] != "Date"]
       df1 = df1[df1[9] != "Page:"]
       df1 = df1[df1[9] != "Date:"]
       df1 = df1[df1[9] != "Time:"]
       '''
       cldf = cldf.append(df1)
       print(cldf.shape)
       return cldf

def walk_doc_lists(directory_path):

    cldf = pd.DataFrame()
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
           file_path   = root + '\\' + filename
#           print(filename)
           if (filename.startswith("gw_docs_")  and filename.endswith(".xls")):
                   print("reading: " + file_path)
                   df1 = pd.read_excel(file_path, sheetname='Sheet1', header=None, index=False)
                   df1 = df1[14:]
                   df1 = df1[[0, 2, 8, 9]]
                   df1 = df1.dropna(axis=0, how='all')
                   df1 = df1[df1[0] != "Note"]
                   df1 = df1[df1[0] != "Date"]
                   df1 = df1[df1[9] != "Page:"]
                   df1 = df1[df1[9] != "Date:"]
                   df1 = df1[df1[9] != "Time:"]
                   cldf = cldf.append(df1)
    print(cldf.shape)
    return cldf

def getCleanDocList(docReport):
#    print("in getClean")
    docsDF = pd.DataFrame()
    i = 0
    totCount = 0
    twoLine = 0
#    docReport = docReport.head(120)
    print("START GET CLEAN")
    print(docReport.shape)
    for x in docReport.index:
#        print(x)       
        row = docReport.iloc[[x]]
    
        i = i + 1
        totCount = totCount + 1
#        print(row.shape)
        date = row.iat[0, 0]
        if i > 999:
            i = 0
            print("Count =" + str(totCount))
        if type(date) == str:
            docDate = valDate(date)
#            '''
            if docDate != None:
                pMRN = parseMRN(docReport, x, 0)
                pName = pMRN[0]
                MRN = pMRN[1]
                pDocType = parseDocType(docReport, x, 0)
#                newRow = pd.DataFrame([[docDate, MRN, pName, pDocType]])
#                docsDF = docsDF.append(newRow)
#            '''
#                return(pMRN)
    return docsDF
def write_cfg(robot, list):
    global pandasData
    if len(list) > 0:
        xlFile =  pandasData + robot + "_cfg.xlsx"
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


patientList = pd.read_csv(pandasData + 'Patient_Demographics.csv', dtype=object)    
        
#patientList = pd.read_csv(pandasData + 'mrn_todo.csv')
#chartList = patientList[patientList['patientSex'] != 'Unknown']
chartList = patientList.dropna(subset=['MRN'])
chartList = chartList['MRN']
rList =  ['ROBOT0', 'ROBOT1', 'ROBOT2',
              'ROBOT3',
              'ROBOT4',
              'ROBOT5',
              'ROBOT7',
              'ROBOT8']
rIter = iter(rList)
numCharts = len(chartList)
print(numCharts)
chartsPerRobot = int(numCharts / 8)
cfgdf = []
i = 1
y = 1

for chart in chartList:
#    print(i)
    if i > chartsPerRobot or y >= numCharts-1:
        i = 1
        try:
            robot = next(rIter)
            print(robot)
            write_cfg(robot, cfgdf)
            cfgdf = []
        except:
            print (i)
    cfgdf = cfgdf + [[str(chart), "NOT"]]
    i = i + 1
    y = y + 1 

       

