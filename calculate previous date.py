import os
import pandas as pd
import requests
import time
from selenium import webdriver
from datetime import date, timedelta
import json
import datetime
# from datetime import datetime

def getLiveStockDataLinks():
    driver = webdriver.Chrome()

    url = "https://siocarnes.magyp.gob.ar/MonitorSioCarnes/MonitorSioCarnes?idAnimal=1&animal=BOVINO#"

    driver.get(url)
    time.sleep(10)

    ul = driver.find_element_by_id('navbarCategorias')
    df = pd.DataFrame()
    for li in ul.find_elements_by_tag_name('li'):
        cat = int(li.get_attribute("data-idcategoria"))
        category = li.text

        print(cat)
        if cat>=1 and cat<=8:
            li.click()
            time.sleep(12)
            subCat = driver.find_element_by_id('subcategoria')
            options = subCat.find_elements_by_tag_name('option')
            for option in options:
                cat2=int(option.get_attribute("data-idcategoria"))
                if cat==cat2:
                    opt = option.get_attribute("Value")
                    code = option.text
                    df = df.append({'Main Category':"BOVINOS", "Category": category,'Subcategory':code,'Code':opt},ignore_index=True)

            # df.to_excel('Category List_Bovine.xlsx',index=False)
            # break

    url = "https://siocarnes.magyp.gob.ar/MonitorSioCarnes/MonitorSioCarnes?idAnimal=2&animal=PORCINO"
    driver.get(url)
    time.sleep(10)

    ul = driver.find_element_by_id('navbarCategorias')
    # df = pd.DataFrame()
    for li in ul.find_elements_by_tag_name('li'):
        cat = int(li.get_attribute("data-idcategoria"))
        category = li.text

        print(cat)
        if cat>=12 and cat<=18:
            li.click()
            time.sleep(12)
            subCat = driver.find_element_by_id('subcategoria')
            options = subCat.find_elements_by_tag_name('option')
            for option in options:
                cat2=int(option.get_attribute("data-idcategoria"))
                if cat==cat2:
                    opt = option.get_attribute("Value")
                    opt = option.get_attribute("Value")
                    code = option.text
                    df = df.append({'Main Category':"PORCINOS", "Category": category, "Category ID": cat ,'Subcategory':code,'Code':opt},ignore_index=True)
            df.to_excel('Category List_All.xlsx',index=False)
    driver.quit()

def getAgroData():

    endDate=date.today()

    # startDate=  datetime.strptime("01-01-2015", '%m-%d-%Y').date()
    last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    startDate = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

    # startDate='2015-01-01'
    startDate=datetime.datetime(2015, 1, 1)
    print(startDate)
    print(endDate)






    dt1 = str('{:02d}'.format(startDate.day))
    mon1= str('{:02d}'.format(startDate.month))
    yr1 = str(startDate.year)


    dt2 = str('{:02d}'.format(endDate.day))
    mon2= str('{:02d}'.format(endDate.month))
    yr2 = str(endDate.year)


    linkdf = pd.read_excel(os.getcwd() + '/agro_mapping.xlsx',sheet_name='Sheet1')

    df = pd.DataFrame()

    for xline in range(len(linkdf)):
        link = linkdf.loc[xline,'link']

        commodity = linkdf.loc[xline,'commodity_name_source']

        link = link.replace("{sdate}",dt1).replace("{smonth}",mon1).replace("{syear}",yr1).replace("{edate}",dt2).replace("{emonth}",mon2).replace("{eyear}",yr2)
        print(commodity)
        print(link)
        # import ipdb;ipdb.set_trace()
        URL= link
        # URL="http://monitorsiogranos.magyp.gob.ar/v5_ajax/caracteristicasZonasFechas_min.php?cosas=%7B%0A++%22fechaDesde%22%3A+%22" + str(dt1) + "%2F" + str(mon1) + "%2F" + str(yr1) + "%22%2C%0A++%22fechaHasta%22%3A+%22" + str(dt2) + "%2F" + str(mon2) + "%2F" + str(yr2) + "%22%2C%0A++%22IDproducto%22%3A+%2217%22%2C%0A++%22IDzona%22%3A+%2224%22%0A%7D"

        # print(URL)
        response = requests.get(URL,verify=False).content

        loaded_json = json.loads(response)

        # import ipdb;ipdb.set_trace()
        for x in loaded_json:
            try:
                dt = str(x['fecha'])
                val1 = str(x['prom_pnd'])
                df = df.append({'commodity_name_source':commodity, 'timeframe_monthly':dt, "value": val1},ignore_index=True)
            except:
                pass



    # df.to_excel('abc.xlsx')

    df['value']=pd.to_numeric(df['value'],errors='coerce')
    df['timeframe_monthly'] =  pd.to_datetime(df['timeframe_monthly'], format='%Y-%m-%d')
    # df.to_excel("All.xlsx",index=False)

    df['Month']=df['timeframe_monthly'].dt.month
    df['Year']=df['timeframe_monthly'].dt.year

    df=df.groupby(['Year','Month','commodity_name_source'], as_index=False)['value'].mean()
    df['dd']=1

    df['timeframe_monthly']=pd.to_datetime((df.Year*10000+df.Month*100+df.dd).apply(str),format='%Y%m%d')
    df=df.drop(['Year','dd','Month'],axis=1)




    df['db_id']=''
    df['is_approved']=''

    df = df[["commodity_name_source", "timeframe_monthly", "value", "db_id", "is_approved"]]

    df=df[df.value != 0]
    df = df[df.value.notnull()]




    file_df=pd.read_excel(os.getcwd()+ '/agro_mapping.xlsx')

    # df = pd.merge(df, file_df, on='commodity_name_source', how='left')
    df=file_df.merge(df,on='commodity_name_source')

    df = df.sort_values(by=['commodity_name','timeframe_monthly'], ascending=[True,False])
    df['timeframe_monthly'] =  df['timeframe_monthly'].dt.strftime('%b-%Y')

    df = df[["db_id", "source_ref", "commodity_name", "commodity_group","Notes", "commodity_grade", "commodity_subgrade", "geography", "unit", "timeframe_monthly", "value" , "is_approved"]]

    # now = datetime.datetime.now()
    # datestring=str(now.year) + '-' + str('{:02d}'.format(now.month)) +'-'+ str(now.day)
    df.to_excel("Agro_Data.xlsx",index=False)

    # df.to_excel("Agro - Data_Historical.xlsx",index=False)


if __name__=="__main__":
    # getLiveStockDataLinks()
    getAgroData()
