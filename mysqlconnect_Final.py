##!/usr/bin/python
#import MySQLdb
#
## Connect
#db = MySQLdb.connect(host="172.22.0.16",
#                     user="root",
#                     passwd="Sc@1234",
#                     db="sma")
#
#cursor = db.cursor()
#
## Execute SQL select statement
#cursor.execute("select  NAICS_Titles,NAICS from Shipment_NAICS_code")
#
## Commit your changes if writing
## In this case, we are only reading data
## db.commit()
#
## Get the number of rows in the resultset
#numrows = cursor.rowcount
#
## Get and display one row at a time
#for x in range(0, numrows):
#    row = cursor.fetchone()
#    print (row[0], "-->", row[1])
#
## Close the connection
#db.close()

#import datetime
import mysql.connector as sql
import pandas as pd

db_connection  = sql.connect(host="172.28.0.11", user='root', database='sma',passwd="Sc@1234")
#
#cursor = cnx.cursor()
#cursor.execute("select  * from cost_data")
#row = cursor.fetchone() 
#pro_info = pd.DataFrame(cursor.fetchall())
#pro_info.to_csv('sample.csv')

df = pd.read_sql('select  * from dummy', con=db_connection)

df=df.apply(lambda x: x.str.replace(',',''))
#df=df.loc[df['time'] == 2012]
#df1=df.loc[df['time'].isin([2012,2014, 2013])] 
#df1=df.describe()
#df['Amount']=df['Amount'].astype('float')
df['Amount'] = pd.to_numeric(df['Amount'],errors='coerce')

Total = df['Amount'].sum()
print (Total)
df.to_csv('sample.csv')

#
#while row is not None:
#    print(row)
#    row = cursor.fetchone()
#
#print (cursor)