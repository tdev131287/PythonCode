import requests
import time
import random
import json
import pandas as pd
import os
import datetime


def CP_Moffcomm():
    
    mstdf = pd.DataFrame()
    
    
    for addCode in range(200,2900):
        
        try:
            url = 'https://account.evgo.com/stationFacade/findStationById?stationId='+str(addCode)
            print(url)
    #        url = 'https://account.evgo.com/stationFacade/findStationById?stationId=1000'
            x=requests.get(url)
            x=json.loads(x.text)
            df=pd.DataFrame(x['data']['stationSockets'])
            df['latitude']=x['data']['latitude']
            df['longitude']=x['data']['longitude']
            df['StateName']=x['data']['addressUsaStateName']
            df['StateCode']=x['data']['addressUsaStateCode']
            df['CountryName']=x['data']['addressCountryName']
            df['CountryIso3']=x['data']['addressCountryIso3Code']
            df['CountryIso2']=x['data']['addressCountryIso2Code']
            df['Address1']=x['data']['addressCountryIso2Code']
            df['City']=x['data']['addressCity']
            df['ZipCode']=x['data']['addressZipCode']
    #        df['Region']=x['data']['addressRegion']
            df['ModelName']=x['data']['stationModelName']
            df['chargingSpeed']=x['data']['chargingSpeedId']
            mstdf = mstdf.append(df)
            mstdf.to_excel('Address_Details.xlsx')
        except:
            print('Error :->'+str(url))
    
#    mstdf.to_excel('Address_Details.xlsx')
#    print(df)


if __name__ == '__main__':
    CP_Moffcomm()
