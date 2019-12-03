import requests
import pandas as pd
from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
import glob
import datetime
import openpyxl
from dateutil.relativedelta import relativedelta

now = datetime.datetime.now()
datestring=str(now.year) + '-' + str('{:02d}'.format(now.month)) +'-'+ str('{:02d}'.format(now.day))
folderName= datestring


look_up = {'1': 'JAN', '2': 'FEV', '3': 'MAR', '4': 'ABR', '5': 'MAI',
            '6': 'JUN', '7': 'JUL', '8': 'AGO', '9': 'SET', '10': 'OUT', '11': 'NOV', '12': 'DEZ'}


folderName=os.path.join(os.path.dirname(__file__)) + '/' + 'Downloaded files' + '/'

if not os.path.exists(folderName):
    os.mkdir(folderName)
#all_data = pd.DataFrame() 
all_data = pd.read_excel(folderName + 'Instituto de Economia Agrícola (IEA)_Received_By_Farmer_Prices_Brazil.xlsx') 
cols = [0,2,3,4,5,6]
all_data = all_data[all_data.columns[cols]]

#Tickers=pd.read_excel('file:///' + os.path.join(os.path.dirname(__file__)) + '/mapping.xlsx',sheet_name="Month")



#for Tickers_Loop in range(len(Tickers)):
for x in range(1,3):
#    code=Tickers.loc[Tickers_Loop,'Code']
    now1 = datetime.date.today() + relativedelta(months=-x)
    
    year=str(now1.year)
    month=str(now1.month)
    code=year+'/'+look_up[month]
    print('Fetching:- ' + code)
    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Origin': 'http://ciagri.iea.sp.gov.br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://ciagri.iea.sp.gov.br/nia1/precos_medios.aspx?cod_sis=2',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
}

    params = (
        ('cod_sis', '2'),
    )

    data = {
      '__VIEWSTATE': '/wEPDwUKMTU0NjU3NTQ3Mg8WBh4LYXV0ZW50aWNhZG8FAU4eF0xvZ2luVXN1YXJpb0F1dGVudGljYWRvZR4IeENvZF9TaXMFATIWAgICD2QWGAIBD2QWAgIBD2QWBgIBDw8WBB4LTmF2aWdhdGVVcmwFQn4vTG9naW4uYXNweD9VcmxSZXRvcm5vPSUyZm5pYTElMmZwcmVjb3NfbWVkaW9zLmFzcHglM2Zjb2Rfc2lzJTNkMh4HVmlzaWJsZWdkZAIDDw8WAh4EVGV4dAUHT2zDoSwgLmRkAgUPDxYCHwMFQ34vTG9nb3V0LmFzcHg/VXJsUmV0b3Jubz0lMmZuaWExJTJmcHJlY29zX21lZGlvcy5hc3B4JTNmY29kX3NpcyUzZDJkZAIDDw8WAh8FBUU8Y2VudGVyPlByZcOnb3MgTcOpZGlvcyBNZW5zYWlzIFJlY2ViaWRvcyBwZWxvcyBBZ3JpY3VsdG9yZXM8L2NlbnRlcj5kZAIJDxAPFggeDEF1dG9Qb3N0QmFja2geDURhdGFUZXh0RmllbGQFCWRlc2NfcHJvZB4ORGF0YVZhbHVlRmllbGQFCGNvZF9wcm9kHgtfIURhdGFCb3VuZGcWAh4Hb25jbGljawU/amF2YXNjcmlwdDpNYXJjYXJfRGVzbWFyY2FyX0NoZWNrYm94KCdjaGtUb2RvcycsJ2Noa0xzdEl0ZW5zJyk7EBU/E0FsZ29kw6NvIGVtIGNhcm/Dp28RQWxnb2TDo28gZW0gcGx1bWERQW1lbmRvaW0gZW0gY2FzY2EOQXJyb3ogZW0gY2FzY2ENQmFuYW5hIG5hbmljYQxCYW5hbmEgcHJhdGEGQmF0YXRhB0JlemVycm8JQm9pIGdvcmRvE0JvaSBnb3JkbyByYXN0cmVhZG8JQm9pIG1hZ3JvEkJvcnJhY2hhKGNvw6FndWxvKQxCdXJybyBkb21hZG8cQ2Fmw6kgYmVuZWYuIGNlcmVqYSBkZXNjYXNjLhxDYWbDqSBiZW5lZi4gc2VjYWdlbSBuYXR1cmFsDUNhZsOpIGVtIGNvY28TQ2Fmw6kgZW0gY29jbyByZW5kYQ9DYW5hIGRlIGHDp3VjYXIGQ2FzdWxvBkNlYm9sYQdGZWlqw6NvEUZyYW5nbyBwYXJhIGNvcnRlB0dhcnJvdGUXTGFyYW5qYSBwYXJhIGluZMO6c3RyaWERTGFyYW5qYSBwYXJhIG1lc2ERTGVpdMOjbyBkZSByZWNyaWEVTGVpdGUgY3J1IHJlZnJpZ2VyYWRvDUxlaXRlIHRpcG8gQiAMTGVpdGUgdGlwbyBDBkxpbcOjbwZNYW1vbmEYTWFuZGlvY2EgcGFyYSBpbmTDunN0cmlhEk1hbmRpb2NhIHBhcmEgbWVzYQdNYXJydWNvJE1lbCBkZSBBYmVsaGEgQ29tdW0gKG7Do28gb3Jnw6JuaWNvKQVNaWxobwdOb3ZpbGhhD092b3MgZGUgY29kb3JuYQ9Pdm9zIHRpcG8gZXh0cmEQT3ZvcyB0aXBvIGdyYW5kZRVPdm9zIHRpcG8gaW5kw7pzdHJpYWwQT3ZvcyB0aXBvIG3DqWRpbxFPdm9zIHRpcG8gcGVxdWVubxZQb2VkZWlyYSBkZXNjYXJ0ZSBsZXZlGFBvZWRlaXJhIGRlc2NhcnRlIHBlc2FkYQRTb2phBVNvcmdvEVN1w61ubyBwYXJhIGFiYXRlHFN1w61ubyBwYXJhIGFiYXRlIHRpcG8gYmFuaGEJVGFuZ2VyaW5hFlRvbWF0ZSBwYXJhIGluZMO6c3RyaWEQVG9tYXRlIHBhcmEgbWVzYQVUb3VybwVUcmlnbwlUcml0aWNhbGUUVmFjYSBkZSBjcmlhciBtYXRyaXoKVmFjYSBnb3JkYR9WYWNhIGxlaXRlaXJhIGFjaW1hIGRlIDEwIGwvZGlhHlZhY2EgbGVpdGVpcmEgYWNpbWEgZGUgMjBsL2RpYRpWYWNhIGxlaXRlaXJhIGF0w6kgNSBsL2RpYR1WYWNhIGxlaXRlaXJhIGRlIDEwIGEgMjBsL2RpYR1WYWNhIGxlaXRlaXJhIGRlIDUgYSAxMCBsL2RpYQpWYWNhIG1hZ3JhFT8EMTEwMQQxMTAzBDExMDIEMTEwNQQxMzA0BDEzMDYEMTEwNgQxNDA3BDE0MTEEMTkxNwQxNDEwBDExMDcEMTQyMQQxMDU1BDEwNTMEMTA1MgQxMDUxBDExMDkEMTEzMgQxMTExBDExMTMEMTQyNgQxNDA4BDEzMTEEMTMxMgQxNDAxBDE5MjAEMTQyMgQxNDIzBDE4MTIEMTExOAQxMTE5BDExMjAEMTQxNgQxMTIxBDExMjQEMTQwOQQxNDQzBDE0MjgEMTQyOQQxNDMyBDE0MzAE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c3A7ZGQCBQ8PFgIfBQUGJm5ic3A7ZGQCAg9kFgxmDw8WAh8FBQYmbmJzcDtkZAIBDw8WAh8FBQYmbmJzcDtkZAICDw8WAh8FBQYmbmJzcDtkZAIDDw8WAh8FBQYmbmJzcDtkZAIEDw8WAh8FBQYmbmJzcDtkZAIFDw8WAh8FBQYmbmJzcDtkZAInDw8WBB8FBThDYW5hLWRlLUHDp8O6Y2FyIGFsdGVyYcOnw6NvIG1haW8gMjAxNSAtIHZlciBtZXRvZG9sb2dpYR8EZ2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxZDBRFpbWdCdG5NZXRvZG9sb2dpYQUNY2hrTHN0SXRlbnMkMAUNY2hrTHN0SXRlbnMkMQUNY2hrTHN0SXRlbnMkMgUNY2hrTHN0SXRlbnMkMwUNY2hrTHN0SXRlbnMkNAUNY2hrTHN0SXRlbnMkNQUNY2hrTHN0SXRlbnMkNgUNY2hrTHN0SXRlbnMkNwUNY2hrTHN0SXRlbnMkOAUNY2hrTHN0SXRlbnMkOQUOY2hrTHN0SXRlbnMkMTAFDmNoa0xzdEl0ZW5zJDExBQ5jaGtMc3RJdGVucyQxMgUOY2hrTHN0SXRlbnMkMTMFDmNoa0xzdEl0ZW5zJDE0BQ5jaGtMc3RJdGVucyQxNQUOY2hrTHN0SXRlbnMkMTYFDmNoa0xzdEl0ZW5zJDE3BQ5jaGtMc3RJdGVucyQxOAUOY2hrTHN0SXRlbnMkMTkFDmNoa0xzdEl0ZW5zJDIwBQ5jaGtMc3RJdGVucyQyMQUOY2hrTHN0SXRlbnMkMjIFDmNoa0xzdEl0ZW5zJDIzBQ5jaGtMc3RJdGVucyQyNAUOY2hrTHN0SXRlbnMkMjUFDmNoa0xzdEl0ZW5zJDI2BQ5jaGtMc3RJdGVucyQyNwUOY2hrTHN0SXRlbnMkMjgFDmNoa0xzdEl0ZW5zJDI5BQ5jaGtMc3RJdGVucyQzMAUOY2hrTHN0SXRlbnMkMzEFDmNoa0xzdEl0ZW5zJDMyBQ5jaGtMc3RJdGVucyQzMwUOY2hrTHN0SXRlbnMkMzQFDmNoa0xzdEl0ZW5zJDM1BQ5jaGtMc3RJdGVucyQzNgUOY2hrTHN0SXRlbnMkMzcFDmNoa0xzdEl0ZW5zJDM4BQ5jaGtMc3RJdGVucyQzOQUOY2hrTHN0SXRlbnMkNDAFDmNoa0xzdEl0ZW5zJDQxBQ5jaGtMc3RJdGVucyQ0MgUOY2hrTHN0SXRlbnMkNDMFDmNoa0xzdEl0ZW5zJDQ0BQ5jaGtMc3RJdGVucyQ0NQUOY2hrTHN0SXRlbnMkNDYFDmNoa0xzdEl0ZW5zJDQ3BQ5jaGtMc3RJdGVucyQ0OAUOY2hrTHN0SXRlbnMkNDkFDmNoa0xzdEl0ZW5zJDUwBQ5jaGtMc3RJdGVucyQ1MQUOY2hrTHN0SXRlbnMkNTIFDmNoa0xzdEl0ZW5zJDUzBQ5jaGtMc3RJdGVucyQ1NAUOY2hrTHN0SXRlbnMkNTUFDmNoa0xzdEl0ZW5zJDU2BQ5jaGtMc3RJdGVucyQ1NwUOY2hrTHN0SXRlbnMkNTgFDmNoa0xzdEl0ZW5zJDU5BQ5jaGtMc3RJdGVucyQ2MAUOY2hrTHN0SXRlbnMkNjEFDmNoa0xzdEl0ZW5zJDYyBQ5jaGtMc3RJdGVucyQ2MgUIY2hrVG9kb3MFDGltZ1Blc3F1aXNhcmI1XXGT+4EMoH72TBYrAiRYww4M',
      '__EVENTVALIDATION': '/wEWcAL7zK+oBQLpluuLCALBtujPAQLAtujPAQK/tujPAQK+tujPAQK9tujPAQK8tujPAQK7tujPAQK6tujPAQK5tujPAQK4tujPAQLAtqjOAQLAtqTOAQLAtrDOAQLAtqzOAQLAtpjOAQLAtpTOAQLAtqDOAQLAtpzOAQLAtsjOAQLAtsTOAQK/tqjOAQK/tqTOAQK/trDOAQK/tqzOAQK/tpjOAQK/tpTOAQK/tqDOAQK/tpzOAQK/tsjOAQK/tsTOAQK+tqjOAQK+tqTOAQK+trDOAQK+tqzOAQK+tpjOAQK+tpTOAQK+tqDOAQK+tpzOAQK+tsjOAQK+tsTOAQK9tqjOAQK9tqTOAQK9trDOAQK9tqzOAQK9tpjOAQK9tpTOAQK9tqDOAQK9tpzOAQK9tsjOAQK9tsTOAQK8tqjOAQK8tqTOAQK8trDOAQK8tqzOAQK8tpjOAQK8tpTOAQK8tqDOAQK8tpzOAQK8tsjOAQK8tsTOAQK7tqjOAQK7tqTOAQK7trDOAQKW9ILsCQL+gr/mBALKp9S8DAL+gpOHAgLRlb26DAL+grfoCQK6k8HkDgK6k/muDAKA0KDgCQLKp9jnDQK6k4XaDgLoruG/AQLKp9z2BAL+guPPDALKp5iEBAL+gtfsCgLRleGDBAL+gvOSBQK6k4XMBgK6k+2CCQKA0MwfAsqnzNsGArqT+Y4IAtXpp+EGAtXpp+EGAuHMzLsOAtXpCwL6/qW9DgLV6a/vCwKR+NnjDAKR+OGpDgKru7jnCwLhzMDgDwKR+J3dDALDxfm4AwLhzMTxBgLV6fvIDgLhzICDBgLV6c/rCAL6/vmEBgLV6euVBwKR+J3LBAKR+PWFCwKru9SYAgLhzNTcBAKR+OGJCgKLtPvqDluci0mfbJQrbYvGe9S/a+KL7yTe',
      'chkLstItens$0': 'on',
      'chkLstItens$1': 'on',
      'chkLstItens$2': 'on',
      'chkLstItens$3': 'on',
      'chkLstItens$4': 'on',
      'chkLstItens$5': 'on',
      'chkLstItens$6': 'on',
      'chkLstItens$7': 'on',
      'chkLstItens$8': 'on',
      'chkLstItens$9': 'on',
      'chkLstItens$10': 'on',
      'chkLstItens$11': 'on',
      'chkLstItens$12': 'on',
      'chkLstItens$13': 'on',
      'chkLstItens$14': 'on',
      'chkLstItens$15': 'on',
      'chkLstItens$16': 'on',
      'chkLstItens$17': 'on',
      'chkLstItens$18': 'on',
      'chkLstItens$19': 'on',
      'chkLstItens$20': 'on',
      'chkLstItens$21': 'on',
      'chkLstItens$22': 'on',
      'chkLstItens$23': 'on',
      'chkLstItens$24': 'on',
      'chkLstItens$25': 'on',
      'chkLstItens$26': 'on',
      'chkLstItens$27': 'on',
      'chkLstItens$28': 'on',
      'chkLstItens$29': 'on',
      'chkLstItens$30': 'on',
#      'chkLstItens$31': 'on',
#      'chkLstItens$32': 'on',
#      'chkLstItens$33': 'on',
#      'chkLstItens$34': 'on',
#      'chkLstItens$35': 'on',
#      'chkLstItens$36': 'on',
#      'chkLstItens$37': 'on',
#      'chkLstItens$38': 'on',
#      'chkLstItens$39': 'on',
#      'chkLstItens$40': 'on',
#      'chkLstItens$41': 'on',
#      'chkLstItens$42': 'on',
#      'chkLstItens$43': 'on',
#      'chkLstItens$44': 'on',
#      'chkLstItens$45': 'on',
#      'chkLstItens$46': 'on',
#      'chkLstItens$47': 'on',
#      'chkLstItens$48': 'on',
#      'chkLstItens$49': 'on',
#      'chkLstItens$50': 'on',
#      'chkLstItens$51': 'on',
#      'chkLstItens$52': 'on',
#      'chkLstItens$53': 'on',
#      'chkLstItens$54': 'on',
#      'chkLstItens$55': 'on',
#      'chkLstItens$56': 'on',
#      'chkLstItens$57': 'on',
#      'chkLstItens$58': 'on',
#      'chkLstItens$59': 'on',
#      'chkLstItens$60': 'on',
#      'chkLstItens$61': 'on',
#      'chkLstItens$62': 'on',
#      'chkTodos': 'on',
      'cmbPeriodo_Inicial': code,
      'cmbPeriodo_Final': code,
      'imgPesquisar.x': '31',
      'imgPesquisar.y': '15'
    }
    
    response = requests.post('http://ciagri.iea.sp.gov.br/nia1/precos_medios.aspx', headers=headers, params=params, data=data, verify=False)
       
    
    df_list = pd.read_html(response.text,header=0)
    df = df_list[-1]
    df=df[:-1]
    all_data = all_data.append(df)
    
    
    
    
    data = {
      '__VIEWSTATE': '/wEPDwUKMTU0NjU3NTQ3Mg8WBh4LYXV0ZW50aWNhZG8FAU4eF0xvZ2luVXN1YXJpb0F1dGVudGljYWRvZR4IeENvZF9TaXMFATIWAgICD2QWGAIBD2QWAgIBD2QWBgIBDw8WBB4LTmF2aWdhdGVVcmwFQn4vTG9naW4uYXNweD9VcmxSZXRvcm5vPSUyZm5pYTElMmZwcmVjb3NfbWVkaW9zLmFzcHglM2Zjb2Rfc2lzJTNkMh4HVmlzaWJsZWdkZAIDDw8WAh4EVGV4dAUHT2zDoSwgLmRkAgUPDxYCHwMFQ34vTG9nb3V0LmFzcHg/VXJsUmV0b3Jubz0lMmZuaWExJTJmcHJlY29zX21lZGlvcy5hc3B4JTNmY29kX3NpcyUzZDJkZAIDDw8WAh8FBUU8Y2VudGVyPlByZcOnb3MgTcOpZGlvcyBNZW5zYWlzIFJlY2ViaWRvcyBwZWxvcyBBZ3JpY3VsdG9yZXM8L2NlbnRlcj5kZAIJDxAPFggeDEF1dG9Qb3N0QmFja2geDURhdGFUZXh0RmllbGQFCWRlc2NfcHJvZB4ORGF0YVZhbHVlRmllbGQFCGNvZF9wcm9kHgtfIURhdGFCb3VuZGcWAh4Hb25jbGljawU/amF2YXNjcmlwdDpNYXJjYXJfRGVzbWFyY2FyX0NoZWNrYm94KCdjaGtUb2RvcycsJ2Noa0xzdEl0ZW5zJyk7EBU/E0FsZ29kw6NvIGVtIGNhcm/Dp28RQWxnb2TDo28gZW0gcGx1bWERQW1lbmRvaW0gZW0gY2FzY2EOQXJyb3ogZW0gY2FzY2ENQmFuYW5hIG5hbmljYQxCYW5hbmEgcHJhdGEGQmF0YXRhB0JlemVycm8JQm9pIGdvcmRvE0JvaSBnb3JkbyByYXN0cmVhZG8JQm9pIG1hZ3JvEkJvcnJhY2hhKGNvw6FndWxvKQxCdXJybyBkb21hZG8cQ2Fmw6kgYmVuZWYuIGNlcmVqYSBkZXNjYXNjLhxDYWbDqSBiZW5lZi4gc2VjYWdlbSBuYXR1cmFsDUNhZsOpIGVtIGNvY28TQ2Fmw6kgZW0gY29jbyByZW5kYQ9DYW5hIGRlIGHDp3VjYXIGQ2FzdWxvBkNlYm9sYQdGZWlqw6NvEUZyYW5nbyBwYXJhIGNvcnRlB0dhcnJvdGUXTGFyYW5qYSBwYXJhIGluZMO6c3RyaWERTGFyYW5qYSBwYXJhIG1lc2ERTGVpdMOjbyBkZSByZWNyaWEVTGVpdGUgY3J1IHJlZnJpZ2VyYWRvDUxlaXRlIHRpcG8gQiAMTGVpdGUgdGlwbyBDBkxpbcOjbwZNYW1vbmEYTWFuZGlvY2EgcGFyYSBpbmTDunN0cmlhEk1hbmRpb2NhIHBhcmEgbWVzYQdNYXJydWNvJE1lbCBkZSBBYmVsaGEgQ29tdW0gKG7Do28gb3Jnw6JuaWNvKQVNaWxobwdOb3ZpbGhhD092b3MgZGUgY29kb3JuYQ9Pdm9zIHRpcG8gZXh0cmEQT3ZvcyB0aXBvIGdyYW5kZRVPdm9zIHRpcG8gaW5kw7pzdHJpYWwQT3ZvcyB0aXBvIG3DqWRpbxFPdm9zIHRpcG8gcGVxdWVubxZQb2VkZWlyYSBkZXNjYXJ0ZSBsZXZlGFBvZWRlaXJhIGRlc2NhcnRlIHBlc2FkYQRTb2phBVNvcmdvEVN1w61ubyBwYXJhIGFiYXRlHFN1w61ubyBwYXJhIGFiYXRlIHRpcG8gYmFuaGEJVGFuZ2VyaW5hFlRvbWF0ZSBwYXJhIGluZMO6c3RyaWEQVG9tYXRlIHBhcmEgbWVzYQVUb3VybwVUcmlnbwlUcml0aWNhbGUUVmFjYSBkZSBjcmlhciBtYXRyaXoKVmFjYSBnb3JkYR9WYWNhIGxlaXRlaXJhIGFjaW1hIGRlIDEwIGwvZGlhHlZhY2EgbGVpdGVpcmEgYWNpbWEgZGUgMjBsL2RpYRpWYWNhIGxlaXRlaXJhIGF0w6kgNSBsL2RpYR1WYWNhIGxlaXRlaXJhIGRlIDEwIGEgMjBsL2RpYR1WYWNhIGxlaXRlaXJhIGRlIDUgYSAxMCBsL2RpYQpWYWNhIG1hZ3JhFT8EMTEwMQQxMTAzBDExMDIEMTEwNQQxMzA0BDEzMDYEMTEwNgQxNDA3BDE0MTEEMTkxNwQxNDEwBDExMDcEMTQyMQQxMDU1BDEwNTMEMTA1MgQxMDUxBDExMDkEMTEzMgQxMTExBDExMTMEMTQyNgQxNDA4BDEzMTEEMTMxMgQxNDAxBDE5MjAEMTQyMgQxNDIzBDE4MTIEMTExOAQxMTE5BDExMjAEMTQxNgQxMTIxBDExMjQEMTQwOQQxNDQzBDE0MjgEMTQyOQQxNDMyBDE0MzAE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c3A7ZGQCBQ8PFgIfBQUGJm5ic3A7ZGQCAg9kFgxmDw8WAh8FBQYmbmJzcDtkZAIBDw8WAh8FBQYmbmJzcDtkZAICDw8WAh8FBQYmbmJzcDtkZAIDDw8WAh8FBQYmbmJzcDtkZAIEDw8WAh8FBQYmbmJzcDtkZAIFDw8WAh8FBQYmbmJzcDtkZAInDw8WBB8FBThDYW5hLWRlLUHDp8O6Y2FyIGFsdGVyYcOnw6NvIG1haW8gMjAxNSAtIHZlciBtZXRvZG9sb2dpYR8EZ2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxZDBRFpbWdCdG5NZXRvZG9sb2dpYQUNY2hrTHN0SXRlbnMkMAUNY2hrTHN0SXRlbnMkMQUNY2hrTHN0SXRlbnMkMgUNY2hrTHN0SXRlbnMkMwUNY2hrTHN0SXRlbnMkNAUNY2hrTHN0SXRlbnMkNQUNY2hrTHN0SXRlbnMkNgUNY2hrTHN0SXRlbnMkNwUNY2hrTHN0SXRlbnMkOAUNY2hrTHN0SXRlbnMkOQUOY2hrTHN0SXRlbnMkMTAFDmNoa0xzdEl0ZW5zJDExBQ5jaGtMc3RJdGVucyQxMgUOY2hrTHN0SXRlbnMkMTMFDmNoa0xzdEl0ZW5zJDE0BQ5jaGtMc3RJdGVucyQxNQUOY2hrTHN0SXRlbnMkMTYFDmNoa0xzdEl0ZW5zJDE3BQ5jaGtMc3RJdGVucyQxOAUOY2hrTHN0SXRlbnMkMTkFDmNoa0xzdEl0ZW5zJDIwBQ5jaGtMc3RJdGVucyQyMQUOY2hrTHN0SXRlbnMkMjIFDmNoa0xzdEl0ZW5zJDIzBQ5jaGtMc3RJdGVucyQyNAUOY2hrTHN0SXRlbnMkMjUFDmNoa0xzdEl0ZW5zJDI2BQ5jaGtMc3RJdGVucyQyNwUOY2hrTHN0SXRlbnMkMjgFDmNoa0xzdEl0ZW5zJDI5BQ5jaGtMc3RJdGVucyQzMAUOY2hrTHN0SXRlbnMkMzEFDmNoa0xzdEl0ZW5zJDMyBQ5jaGtMc3RJdGVucyQzMwUOY2hrTHN0SXRlbnMkMzQFDmNoa0xzdEl0ZW5zJDM1BQ5jaGtMc3RJdGVucyQzNgUOY2hrTHN0SXRlbnMkMzcFDmNoa0xzdEl0ZW5zJDM4BQ5jaGtMc3RJdGVucyQzOQUOY2hrTHN0SXRlbnMkNDAFDmNoa0xzdEl0ZW5zJDQxBQ5jaGtMc3RJdGVucyQ0MgUOY2hrTHN0SXRlbnMkNDMFDmNoa0xzdEl0ZW5zJDQ0BQ5jaGtMc3RJdGVucyQ0NQUOY2hrTHN0SXRlbnMkNDYFDmNoa0xzdEl0ZW5zJDQ3BQ5jaGtMc3RJdGVucyQ0OAUOY2hrTHN0SXRlbnMkNDkFDmNoa0xzdEl0ZW5zJDUwBQ5jaGtMc3RJdGVucyQ1MQUOY2hrTHN0SXRlbnMkNTIFDmNoa0xzdEl0ZW5zJDUzBQ5jaGtMc3RJdGVucyQ1NAUOY2hrTHN0SXRlbnMkNTUFDmNoa0xzdEl0ZW5zJDU2BQ5jaGtMc3RJdGVucyQ1NwUOY2hrTHN0SXRlbnMkNTgFDmNoa0xzdEl0ZW5zJDU5BQ5jaGtMc3RJdGVucyQ2MAUOY2hrTHN0SXRlbnMkNjEFDmNoa0xzdEl0ZW5zJDYyBQ5jaGtMc3RJdGVucyQ2MgUIY2hrVG9kb3MFDGltZ1Blc3F1aXNhcmI1XXGT+4EMoH72TBYrAiRYww4M',
      '__EVENTVALIDATION': '/wEWcAL7zK+oBQLpluuLCALBtujPAQLAtujPAQK/tujPAQK+tujPAQK9tujPAQK8tujPAQK7tujPAQK6tujPAQK5tujPAQK4tujPAQLAtqjOAQLAtqTOAQLAtrDOAQLAtqzOAQLAtpjOAQLAtpTOAQLAtqDOAQLAtpzOAQLAtsjOAQLAtsTOAQK/tqjOAQK/tqTOAQK/trDOAQK/tqzOAQK/tpjOAQK/tpTOAQK/tqDOAQK/tpzOAQK/tsjOAQK/tsTOAQK+tqjOAQK+tqTOAQK+trDOAQK+tqzOAQK+tpjOAQK+tpTOAQK+tqDOAQK+tpzOAQK+tsjOAQK+tsTOAQK9tqjOAQK9tqTOAQK9trDOAQK9tqzOAQK9tpjOAQK9tpTOAQK9tqDOAQK9tpzOAQK9tsjOAQK9tsTOAQK8tqjOAQK8tqTOAQK8trDOAQK8tqzOAQK8tpjOAQK8tpTOAQK8tqDOAQK8tpzOAQK8tsjOAQK8tsTOAQK7tqjOAQK7tqTOAQK7trDOAQKW9ILsCQL+gr/mBALKp9S8DAL+gpOHAgLRlb26DAL+grfoCQK6k8HkDgK6k/muDAKA0KDgCQLKp9jnDQK6k4XaDgLoruG/AQLKp9z2BAL+guPPDALKp5iEBAL+gtfsCgLRleGDBAL+gvOSBQK6k4XMBgK6k+2CCQKA0MwfAsqnzNsGArqT+Y4IAtXpp+EGAtXpp+EGAuHMzLsOAtXpCwL6/qW9DgLV6a/vCwKR+NnjDAKR+OGpDgKru7jnCwLhzMDgDwKR+J3dDALDxfm4AwLhzMTxBgLV6fvIDgLhzICDBgLV6c/rCAL6/vmEBgLV6euVBwKR+J3LBAKR+PWFCwKru9SYAgLhzNTcBAKR+OGJCgKLtPvqDluci0mfbJQrbYvGe9S/a+KL7yTe',
      'chkLstItens$0': 'on',
#      'chkLstItens$1': 'on',
#      'chkLstItens$2': 'on',
#      'chkLstItens$3': 'on',
#      'chkLstItens$4': 'on',
#      'chkLstItens$5': 'on',
#      'chkLstItens$6': 'on',
#      'chkLstItens$7': 'on',
#      'chkLstItens$8': 'on',
#      'chkLstItens$9': 'on',
#      'chkLstItens$10': 'on',
#      'chkLstItens$11': 'on',
#      'chkLstItens$12': 'on',
#      'chkLstItens$13': 'on',
#      'chkLstItens$14': 'on',
#      'chkLstItens$15': 'on',
#      'chkLstItens$16': 'on',
#      'chkLstItens$17': 'on',
#      'chkLstItens$18': 'on',
#      'chkLstItens$19': 'on',
#      'chkLstItens$20': 'on',
#      'chkLstItens$21': 'on',
#      'chkLstItens$22': 'on',
#      'chkLstItens$23': 'on',
#      'chkLstItens$24': 'on',
#      'chkLstItens$25': 'on',
#      'chkLstItens$26': 'on',
#      'chkLstItens$27': 'on',
#      'chkLstItens$28': 'on',
#      'chkLstItens$29': 'on',
#      'chkLstItens$30': 'on',
      'chkLstItens$31': 'on',
      'chkLstItens$32': 'on',
      'chkLstItens$33': 'on',
      'chkLstItens$34': 'on',
      'chkLstItens$35': 'on',
      'chkLstItens$36': 'on',
      'chkLstItens$37': 'on',
      'chkLstItens$38': 'on',
      'chkLstItens$39': 'on',
      'chkLstItens$40': 'on',
      'chkLstItens$41': 'on',
      'chkLstItens$42': 'on',
      'chkLstItens$43': 'on',
      'chkLstItens$44': 'on',
      'chkLstItens$45': 'on',
      'chkLstItens$46': 'on',
      'chkLstItens$47': 'on',
      'chkLstItens$48': 'on',
      'chkLstItens$49': 'on',
      'chkLstItens$50': 'on',
      'chkLstItens$51': 'on',
      'chkLstItens$52': 'on',
      'chkLstItens$53': 'on',
      'chkLstItens$54': 'on',
      'chkLstItens$55': 'on',
      'chkLstItens$56': 'on',
      'chkLstItens$57': 'on',
      'chkLstItens$58': 'on',
      'chkLstItens$59': 'on',
      'chkLstItens$60': 'on',
      'chkLstItens$61': 'on',
      'chkLstItens$62': 'on',
#      'chkTodos': 'on',
      'cmbPeriodo_Inicial': code,
      'cmbPeriodo_Final': code,
      'imgPesquisar.x': '31',
      'imgPesquisar.y': '15'
    }
    
    response = requests.post('http://ciagri.iea.sp.gov.br/nia1/precos_medios.aspx', headers=headers, params=params, data=data, verify=False)
           
    df_list = pd.read_html(response.text,header=0)
    df = df_list[-1]
    df=df[:-1]
    all_data = all_data.append(df)


dfmap=pd.read_excel(os.path.join(os.path.dirname(__file__)) + '/' +'mapping.xlsx',sheet_name='Received by Farmers')
result=dfmap.merge(all_data,on='Produto')  
cols = [0,1,2,3,4,5,6]
result = result[result.columns[cols]]

result=result.drop_duplicates(subset=None, keep='first', inplace=False)

result.to_excel(folderName + 'Instituto de Economia Agrícola (IEA)_Received_By_Farmer_Prices_Brazil.xlsx',index=False)
