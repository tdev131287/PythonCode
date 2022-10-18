import requests
import json
import pandas as pd
import os
import datetime

def hwwi_api():
    linkdf = pd.read_excel(os.path.join(os.path.dirname(__file__)) + '/mapping.xlsx',sheet_name='Sheet1')
    cookies = {
        'borlabs-cookie': '%7B%22consents%22%3A%7B%22essential%22%3A%5B%22borlabs-cookie%22%5D%2C%22external-media%22%3A%5B%22facebook%22%2C%22googlemaps%22%2C%22instagram%22%2C%22openstreetmap%22%2C%22twitter%22%2C%22vimeo%22%2C%22youtube%22%5D%7D%2C%22domainPath%22%3A%22www.hwwi-rohindex.de%2F%22%2C%22expires%22%3A%22Tue%2C%2026%20Sep%202023%2005%3A40%3A13%20GMT%22%2C%22uid%22%3A%22naja8nfj-wbsm78w5-5nkkatff-gs4iyycz%22%2C%22version%22%3A%221%22%7D',
        '_icl_visitor_lang_js': 'en_in',
        'wpml_browser_redirect_test': '0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en-IN;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'borlabs-cookie=%7B%22consents%22%3A%7B%22essential%22%3A%5B%22borlabs-cookie%22%5D%2C%22external-media%22%3A%5B%22facebook%22%2C%22googlemaps%22%2C%22instagram%22%2C%22openstreetmap%22%2C%22twitter%22%2C%22vimeo%22%2C%22youtube%22%5D%7D%2C%22domainPath%22%3A%22www.hwwi-rohindex.de%2F%22%2C%22expires%22%3A%22Tue%2C%2026%20Sep%202023%2005%3A40%3A13%20GMT%22%2C%22uid%22%3A%22naja8nfj-wbsm78w5-5nkkatff-gs4iyycz%22%2C%22version%22%3A%221%22%7D; _icl_visitor_lang_js=en_in; wpml_browser_redirect_test=0',
        'Origin': 'https://www.hwwi-rohindex.de',
        'Referer': 'https://www.hwwi-rohindex.de/en/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-WP-Nonce': '219a9a435a',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.post('https://www.hwwi-rohindex.de/en/api/hwwi/v1/chart', cookies=cookies, headers=headers)
    dfres = pd.DataFrame(columns=['Date','value','commodity_name_source'])
    loaded_json=response.json()
    # import ipdb; ipdb.set_trace()
    for key in loaded_json:
        listv = loaded_json[key]
        for item in listv:

            # ts=item[0]
            # dt= datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            # dt=(((int(item[0])/60)/60)/24)+25569
            dt=item[0]
            val=item[1]
            dfres = dfres.append({'Date':dt,'value':val,'commodity_name_source':key},ignore_index=True)


    dfres['Date1'] = dfres['Date'].apply(convertunixData)
    dfres['timeframe_monthly'] =  pd.to_datetime(dfres['Date1'], format='%Y-%m-%d')

    dfres['Month']=dfres['timeframe_monthly'].dt.month
    dfres['Year']=dfres['timeframe_monthly'].dt.year
    dfres=dfres.groupby(['Month','Year','commodity_name_source'], as_index=False)['value'].mean()
    dfres['Day']=1
    dfres['timeframe_monthly'] =pd.to_datetime(dfres[['Year', 'Month', 'Day']])
    dfres=linkdf.merge(dfres,on='commodity_name_source')
    dfres = dfres.sort_values(by=['commodity_name','timeframe_monthly'], ascending=[True,False])
    dfres['timeframe_monthly'] = dfres['timeframe_monthly'].dt.strftime('%b-%Y')

    dfres['is_approved']=''
    dfres['db_id']=''
    dfres = dfres[['db_id','source_ref','commodity_name','commodity_group','notes','commodity_grade','commodity_subgrade', 'geography', 'unit','timeframe_monthly','value','is_approved']]
    dfres.to_excel(os.path.join(os.path.dirname(__file__)) + '/hwwi_final.xlsx',index=False)

    import ipdb; ipdb.set_trace()


    print(response.text)

def convertunixData(date):
    return datetime.datetime.utcfromtimestamp(date/1000).strftime('%Y-%m-%d')
if __name__=="__main__":
    path = os.path.join(os.path.dirname(__file__))
    hwwi_api()
