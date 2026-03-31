import os
from selenium import webdriver
import pandas as pd
import requests
import json
import time

def G2Scraper():
    # url='https://www.g2.com/products/hypeauditor/competitors/alternatives'
    url='https://plus.dmea.de/showfloor/organizations'
    driver = webdriver.Chrome()
    driver.get(url)
    import ipdb;ipdb.set_trace()

def GetAllCompanyName():
    mstdf = pd.DataFrame()

    url = "https://live.messebackend.aws.corussoft.de/webservice/search"

    payload = "topic=2022_DMEA&os=web&appUrl=https%3A%2F%2Fplus.dmea.de&lang=en&apiVersion=52&timezoneOffset=0&numresultrows=769&startresultrow=0&filterlist=entity_orga&order=relevance&secondaryOrder=lexic&desc=false"
    headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'EC-Client': 'EventGuide/2.23.2-10803[52]',
    'EC-Client-Branding': '2022_DMEA',
    'Origin': 'https://plus.dmea.de',
    'Referer': 'https://plus.dmea.de/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'beConnectionToken': 'eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3NzQyNTEyMTksImlzcyI6ImV2ZW50LWNsb3VkLmNvbSIsInN1YiI6IjExNzE1OTY5IiwidHlwZSI6ImJlQ29ubmVjdGlvbiJ9.bYuOKNl16dzf9JN8bX4KIoI9vQR4yO7mb8YKoyQsjMrAsPfqjVQdcXQ4zBDfK7Rqh0akWvN525_E68OaM2siQQ',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Authorization': 'Token {{5fdef596-daf7-4212-a2f0-4231f3213492}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    result = json.loads(response.text)
    for idx in range(0,len(result['entities'])):
        data = result['entities'][idx]['contacts']
        df = pd.DataFrame(data)
        
        df['OrgId']=result['entities'][idx]['id']
        mstdf = mstdf.append(df)
        # import ipdb;ipdb.set_trace()
    mstdf.to_excel('CompanyCode.xlsx')
    # print(response.text)

def NextLevelData():
    
    mstdf = pd.DataFrame()
    dflist = pd.read_excel('CompanyCode.xlsx')
    for idx in range(len(dflist)):
        
        url = "https://live.messebackend.aws.corussoft.de/webservice/companydetails"
        code=dflist.iloc[idx]['OrgId']
        payload = "topic=2022_DMEA&os=web&appUrl=https%3A%2F%2Fplus.dmea.de&lang=en&apiVersion=52&timezoneOffset=0&organizationid="+str(code)+"&hideNewsdata=false&showPersonsEventDates=true&showCategoryHierarchy=true&rootCategories=products_dmea_26"
        headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en-IN;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'EC-Client': 'EventGuide/2.23.2-10803[52]',
        'EC-Client-Branding': '2022_DMEA',
        'Origin': 'https://plus.dmea.de',
        'Referer': 'https://plus.dmea.de/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'beConnectionToken': 'eyJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3NzQyNDg2MDksImlzcyI6ImV2ZW50LWNsb3VkLmNvbSIsInN1YiI6IjExNzE1NjU0IiwidHlwZSI6ImJlQ29ubmVjdGlvbiJ9.CConYHgyRZ_LGe7o-4USjLnSRg17sa1MPSf8c2qg1oYlow4k60oQFQN420AXdrjDN4Po8JPWOsr9YTbwIn0Tsw',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Authorization': 'Token {{5fdef596-daf7-4212-a2f0-4231f3213492}}'
        }

        response = requests.request("POST", url, headers=headers, data=payload,verify=False)
        result = json.loads(response.text)
        website= result['web']
        mstdf = mstdf.append({'Website':website,'Code':code},ignore_index=True)
        mstdf.to_excel('Website.xlsx')
        # import ipdb;ipdb.set_trace()
        # print(response.text)

def ftComScraper():
    # url='https://www.ft.com/content/afd4a379-6332-47bb-bc65-04bd6eb24a19'
    dfAll = pd.DataFrame()
    driver = webdriver.Chrome()
    url='https://flo.uri.sh/visualisation/27759465/embed?auto=20'
    driver.get(url)
    for pg in range(1,21):
        # url = 'https://flo.uri.sh/visualisation/27759465/embed?auto='+str(pg)
        # print(url)
        try:
            # import ipdb;ipdb.set_trace()
            # sec = driver.find_elements_by_id('fl-layout-primary-container')[0]
            tbl = driver.find_elements_by_id('table-inner')[0]
            tr= tbl.find_elements_by_css_selector("[class='tr body-row']")[0]
            for tr in tbl.find_elements_by_css_selector("[class='tr body-row']"):
                name = tr.find_elements_by_css_selector("[class='td']")[1].text
                website =tr.find_elements_by_css_selector("[class='td']")[1].find_elements_by_tag_name('a')[0].get_attribute('href')
                country=tr.find_elements_by_css_selector("[class='td']")[2].text
                sector=tr.find_elements_by_css_selector("[class='td']")[3].text
                absGrowth=tr.find_elements_by_css_selector("[class='td']")[4].text
                cmpAnnual=tr.find_elements_by_css_selector("[class='td']")[5].text
                rev2024=tr.find_elements_by_css_selector("[class='td']")[6].text
                rev2021=tr.find_elements_by_css_selector("[class='td']")[7].text
                dfAll = dfAll.append({'Name':name,'Website':website,'Country':country,'Sector':sector,
                                    'AbsGrowth':absGrowth,'Compound Growth':cmpAnnual,'Revenue2024':rev2024,'Revenue2021':rev2021,'PageNumber':pg},ignore_index=True)
            print('Click for Next page --- :'+str(pg))
            driver.find_elements_by_css_selector("[class='pagination-btn next']")[0].click()
            time.sleep(3)
            dfAll.to_excel('Result02.xlsx',index=False)
        except:
            pass

if __name__=="__main__":
    # G2Scraper()
    # GetAllCompanyName()
    # NextLevelData()
    ftComScraper()