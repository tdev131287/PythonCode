import requests
import openpyxl as xl
import json
import os
import time
import datetime
from selenium import webdriver
import pandas as pd
import time


#############Example 1
    
#url='http://www.asianmetal.com/price/ajax/getProductPrice.am'
#
#
#response = requests.get(url)
#print(response.json())
#loaded_json=response.json()
#
#
#df = pd.DataFrame(loaded_json["l"]) 
#df.to_excel('data1.xlsx',index=False)




####Example 2

#url='https://api.ons.gov.uk/dataset/MM23/timeseries/dohn/data'
#
#
#response = requests.get(url)
#print(response.json())
#loaded_json=response.json()
#
#
#df = pd.DataFrame(loaded_json["months"]) 
#df.to_excel('data2.xlsx',index=False)


####example 3

#url='https://aip.com.au/aip-api-request?api-path=public/api&call=retailNationalUlp&location=National+Average'
#
#
#response = requests.get(url)
#print(response.json())
#loaded_json=response.json()
#
#
#df = pd.DataFrame(loaded_json["series"]) 
#df.to_excel('data3.xlsx',index=False)


####example 4


# turl='http://price.mofcom.gov.cn/pricequotation/pricequotationdetail.shtml?seqno=248'
url = 'http://price.mofcom.gov.cn/datamofcom/front/price/pricequotation/priceQueryList'
data = {"seqno": '54', "startTime": 2017, "endTime":2020, "pageNumber":1, "pageSize":10000}
x=requests.post(url, data=data) 
loaded_json=json.loads(x.text)
df = pd.DataFrame(loaded_json["rows"]) 
df['code']=54
df.to_excel('data4.xlsx',index=False)




