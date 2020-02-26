# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 17:19:34 2020

@author: Devendra.Tripathi
"""

import pandas as pd
import MySQLdb
import pandas.io.sql as psql
from sqlalchemy import create_engine
import glob
import os
import matplotlib.pyplot as plt

class AgMarketCommodity:
    
    def Import_Commodity(self):
        engine = create_engine("mysql+pymysql://{user}:{pw}@172.28.0.11/{db}"
                       .format(user="root",
                               pw="Sc@1234",
                               db="scraping"))
        directory=os.path.join(os.path.dirname(__file__))+ '/Commodity/'
        os.chdir(directory)
        files=glob.glob('*.csv*')
        for file in files:
#            print('File Name : ->' + directory+file)
            agdf = pd.read_csv(directory+file,index_col=0)
            
            agdf.to_sql('amphophalus', con = engine, if_exists = 'append', chunksize = 1000)
            print('Data Inserted' + file)
            
        # close the database connection
        
        
    def Commodity_MaxDate(self):
        db=MySQLdb.connect(host='172.28.0.11', user='root', passwd='Sc@1234', db='scraping')
        # create the query
        query = "select * from amphophalus"
        # execute the query and assign it to a pandas dataframe
        df = psql.read_sql(query, con=db)
        
#        uniqueDf = df.groupby(["Commodity","Price Date"],as_index=False).count().reset_index()
#        uniqueDf = df.groupby("Commodity")["Price Date"].max()
        uniqueDf=df.groupby(['Commodity'])['Price Date'].agg('max').reset_index()
        uniqueDf.to_excel('UniqueName.xlsx',index=False)
        db.close()
    
    def Analysis_Single_Commodity(self,commodity):
        db=MySQLdb.connect(host='172.28.0.11', user='root', passwd='Sc@1234', db='scraping')
        query = "select * from amphophalus"
        df = psql.read_sql(query, con=db)
        df =df[df['Commodity']==commodity]
#        df.plot(x ='Min Price (Rs./Quintal)', y='Max Price (Rs./Quintal)', kind = 'scatter')
        df.plot(x ='Price Date', y='Max Price (Rs./Quintal)', kind = 'line')
        plt.show()
            
obj = AgMarketCommodity()
#obj.Import_Commodity()
obj.Commodity_MaxDate()
obj.Analysis_Single_Commodity('Amla(Nelli Kai)')