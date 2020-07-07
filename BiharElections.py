# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:13:57 2020

@author: Devendra.Tripathi
"""
import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def GetDetails():
    url='http://vidhansabha.bih.nic.in/Knowyourmla.html'
    html = requests.get(url).content
    time.sleep(10)

    df_list = pd.read_html(html)
    df =  df_list[-1]
    
    df.to_excel('Bihar_Vidhayak.xlsx',index=False)

def download_pdf():
    url='http://vidhansabha.bih.nic.in/Knowyourmla.html'
    
    filepath = "E:\\Projects\\Elections"
    
    urllist=[]
#    
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : filepath,"plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    s1= Select(driver.find_element_by_name('example_length'))
    s1.select_by_index(3)
#    import ipdb;ipdb.set_trace()
    tbl = driver.find_elements_by_tag_name('table')[0]
    for tr in tbl.find_elements_by_tag_name('tr'):
        try:
            url = tr.find_elements_by_tag_name('td')[2].find_elements_by_tag_name('a')[0].get_attribute('href')
            print(url)
            urllist.append(url)
        except:
            print('link not there')
  
    for linkinfo in urllist:
        driver.get(linkinfo)
    
    driver.quit()
if __name__=="__main__":
#    GetDetails()
    download_pdf()