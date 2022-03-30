import os
import glob
import requests
import json
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


# download file
def AustralianInstituteofPetroleum():
    # mstdf = pd.DataFrame(columns=['Date','value','Commodity_Name_Source'])
    # pddf =pd.DataFrame()
    # folderName=os.path.join(os.path.dirname(__file__)) + '/Download/'

    # if not os.path.exists(folderName):
    #     os.mkdir(folderName)
    # URL_list=[
    #         "https://aip.com.au/aip-api-request?api-path=public/api&call=retailNationalUlp&location=National+Average",
    #         "https://aip.com.au/aip-api-request?api-path=public/api&call=retailNationalDiesel&location=National+Average"
    #         ]
    # fl_list=[
    #         'Petrol',
    #         'Diesel'
    #         ]
    # findex=0

    linkdf = pd.read_excel(os.getcwd() + '/mapping.xlsx',sheet_name='Sheet1')
    dfall = pd.DataFrame()

    for xline in range(len(linkdf)):
        url = linkdf.loc[xline,'API']
        name = linkdf.loc[xline,'commodity_name_source']


        response = requests.get(url,verify=False).content

        loaded_json = json.loads(response)

        x=loaded_json['series']
        dfdata=pd.DataFrame(x[0]['data'])
        dfdata.columns=["Date", "value"]
        dfdata['commodity_name_source']=name
        dfall=dfall.append(dfdata)


    dfall['Date1'] = dfall['Date'].apply(convertunixData)
    dfall['timeframe_monthly'] =  pd.to_datetime(dfall['Date1'], format='%Y-%m-%d')
    # import ipdb; ipdb.set_trace()

    dfall['Month']=dfall['timeframe_monthly'].dt.month
    dfall['Year']=dfall['timeframe_monthly'].dt.year
    dfall=dfall.groupby(['Month','Year','commodity_name_source'], as_index=False)['value'].mean()
    dfall['Day']=1
    dfall['timeframe_monthly'] =pd.to_datetime(dfall[['Year', 'Month', 'Day']])
    dfall=linkdf.merge(dfall,on='commodity_name_source')
    dfall = dfall.sort_values(by=['commodity_name','timeframe_monthly'], ascending=[True,False])
    dfall['timeframe_monthly'] = dfall['timeframe_monthly'].dt.strftime('%b-%Y')

    dfall['is_approved']=''
    dfall['db_id']=''
    dfall = dfall[['db_id','source_ref','commodity_name','commodity_group','notes','commodity_grade','commodity_subgrade', 'geography', 'unit','timeframe_monthly','value','is_approved']]
    dfall.to_excel(os.getcwd() + '/AustralianInstituteofPetroleum_Data_final.xlsx',index=False)

def convertunixData(date):

    return datetime.datetime.utcfromtimestamp(date/1000).strftime('%Y-%m-%d')


if __name__=="__main__":

    AustralianInstituteofPetroleum()
