# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:29:11 2019

@author: Devendra.Tripathi
"""

import pyodbc 
#cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
#                      "Server=172.28.0.11;"
#                      "Database=tscKDTDatabase;"
#                      "Trusted_Connection=yes;")

cnxn = pyodbc.connect("Driver = {SQL Server Native Client 11.0};"               
               "Server=172.28.0.11;"
               "Database=tscKDTDatabase;"
               "username = SMAUser;"
               "password = SMA@2017;"
               "Trusted_Connection = yes;")
cursor = cnxn.cursor()
cursor.execute('SELECT * FROM Master_SunSirs')

for row in cursor:
    print('row = %r' % (row,))