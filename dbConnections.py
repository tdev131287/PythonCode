import pandas as pd
import pyodbc
import os
import numpy as np
from selenium import webdriver
import time
def SqlConnection():
    server = '172.21.1.78'
    database = 'Tata365'
    username = 'Tata365User'
    password = 'Admin365'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    df = pd.read_csv('https://data.cityofnewyork.us/api/views/ipu4-2q9a/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*')

    for index, row in df.iterrows():
        import ipdb; ipdb.set_trace()
         # cursor.execute("INSERT INTO HumanResources.DepartmentTest (DepartmentID,Name,GroupName) values(?,?,?)", row.DepartmentID, row.Name, row.GroupName)
    cnxn.commit()
    cursor.close()

def MSAccessConnection():
    path = os.path.join(os.path.dirname(__file__))
    dbpath=path + '/Building.accdb'
    conn_str = ('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+ dbpath +';')
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    # df = pd.read_csv('https://data.cityofnewyork.us/api/views/ipu4-2q9a/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*')
    # sql='''Insert into [Master_SunSirs]([Link],[Commodity],[Sector],[Value],[Data_Date]) values (?,?,?,?,?);'''

def splitin_Chunks():
    n=50000
    # df = pd.read_excel(fpath+'/Sample.xlsx')
    df = pd.read_csv('https://data.cityofnewyork.us/api/views/ipu4-2q9a/rows.csv?accessType=DOWNLOAD&bom=true&query=select+*')
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]
    # list_df = np.array_split(df, n)
    for index in range(0,len(list_df)):
        reqdf = list_df[index]
        reqdf.to_excel(fpath+'/Building-info'+str(index)+'.xlsx',index=False)
    # import ipdb; ipdb.set_trace()

def AppendMSAccess():
    path = os.path.join(os.path.dirname(__file__))
    dbpath=path + '/Building.accdb'
    conn_str = ('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+ dbpath +';')
    cnxn = pyodbc.connect(conn_str)
    Alldata = pd.DataFrame()
    Alldata = pd.read_excel(path+'\\Building-info0.xlsx')
    print(Alldata)
    crsr = cnxn.cursor()
    sql='''Insert into [BuildingData]([BOROUGH],[Bin #],[House #],[Street Name],[Job #],[Job doc #],[Job Type],[Self_Cert],
    [Block],[Lot],[Community Board],[Zip Code],[Bldg Type],[Residential],[Special District 1],[Special District 2],[Work Type],
    [Permit Status],[Filing Status],[Permit Type],[Permit Sequence #],[Permit Subtype],[Oil Gas],[Site Fill],[Filing Date],
    [Issuance Date],[Expiration Date],[Job Start Date],[Permittee's First Name],[Permittee's Last Name],[Permittee's Business Name],
    [Permittee's Phone #],[Permittee's License Type],[Permittee's License #],[Act as Superintendent],[Permittee's Other Title],
    [HIC License],[Site Safety Mgr's First Name],[Site Safety Mgr's Last Name],[Site Safety Mgr Business Name],
    [Superintendent First & Last Name],[Superintendent Business Name],[Owner's Business Type],[Non-Profit],[Owner's Business Name],
    [Owner's First Name],[Owner's Last Name],[Owner's House #],[Owner's House Street Name],[Owner’s House City],[Owner’s House State],
    [Owner’s House Zip Code],[Owner's Phone #],[DOBRunDate],[PERMIT_SI_NO],[LATITUDE],[LONGITUDE],[COUNCIL_DISTRICT],[CENSUS_TRACT],
    [NTA_NAME]) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
    crsr.executemany(sql, Alldata.itertuples(index=False))
    cnxn.commit()
    crsr.commit()


    dfError.to_excel('Errorlog.xlsx',index=False)
def skyscrapercenter_com():
    url ='https://www.skyscrapercenter.com/building/the-shard/451#facts'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    # import ipdb; ipdb.set_trace()
    infoObj= driver.find_elements_by_css_selector("[class='flex flex-wrap']")[0]
    for info in driver.find_elements_by_css_selector("[class='flex row w-full px-4']"):
        heading = info.find_elements_by_css_selector("[class='w-1/2']")[0].text
        value = info.find_elements_by_css_selector("[class='w-1/2']")[1].text
        print('Heading - >>> ' + str(heading))
        # import ipdb; ipdb.set_trace()


if __name__=="__main__":
    fpath=os.path.join(os.path.dirname(__file__))
    # MSAccessConnection()
    # splitin_Chunks()
    # AppendMSAccess()
    skyscrapercenter_com()
