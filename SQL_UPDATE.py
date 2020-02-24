# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 11:37:59 2019

@author: Devendra.Tripathi
"""

import pandas as pd
#import pyodbc
import mysql.connector
import os
import glob
from sqlalchemy import create_engine

#path='D:\\COE Automation\\Anuj Madan\\API-Data\\USDA\\downloaded files\\0111000_2000.xlsx'

class SmartTask:
    def Import_Excel_to_SQL(self):
#        directory=os.path.join(os.path.dirname(__file__))+ '/USDA/downloaded files/'
        directory=os.path.join(os.path.dirname(__file__))+ '/Mapping/'
        os.chdir(directory)
        files=glob.glob('*.xls*')
        #engine = create_engine('mssql+pyodbc://SMAUser:SMA@2017@pythondsn')
        engine = create_engine('mysql+mysqlconnector://root@localhost:3306/tscdatabase')


        for filename in files:
            print(filename)
#            path =os.path.join(os.path.dirname(__file__))+ '/USDA/downloaded files/' + filename
            path =os.path.join(os.path.dirname(__file__))+ '/Mapping/' + filename
            usddf=pd.read_excel(path,index_col=0)
            usddf.to_sql('datemapping', con=engine, if_exists='append',index=False)
            
    def Resample_Yearly_to_Monthly(self):pass
        
        directory=os.path.join(os.path.dirname(__file__))+ '/USDA/downloaded files/'
        os.chdir(directory)
        files=glob.glob('*.xls*')
        engine = create_engine('mssql+pyodbc://SMAUser:SMA@2017@pythondsn')
        path='D:\\COE Automation\\Anuj Madan\\API-Data\\USDA\\downloaded files\\0111000_2000.xlsx'
        usddf=pd.read_excel(path,index_col=0)
        

obj =SmartTask()
obj.Import_Excel_to_SQL()            
usddf.to_sql("mst_rData_USDA", engine)

tmp_df=usddf.iloc[:, 1:11] # first five rows of dataframe
usddf.to_excel('abc.xlsx')
print(tmp_df.head(10))


