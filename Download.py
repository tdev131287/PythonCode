# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:53:37 2020

@author: Devendra.Tripathi
"""

import pandas as pd
from selenium import webdriver
import os
# import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
#options.add_argument("silent")

#chrome_options.headless = True
driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(__file__))+'\chromedriver.exe',chrome_options=options)


driver.get('https://covid19.apple.com/mobility')

# time.sleep(3)
div = driver.find_elements_by_css_selector("[class='download-button-container']")[0]
a=div.find_elements_by_tag_name('a')[0]

url=a.get_attribute('href')
print(url)
driver.quit()

df = pd.read_csv(url)
df.to_csv(os.path.join(os.path.dirname(__file__))+'\DataDump.csv',index=False)
