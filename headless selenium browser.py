from urllib.parse import parse_qsl
import ipdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as t1
import os
import pandas as pd
import requests
import csv
from datetime import *
import pandas as pd
import shutil
import glob
# from datetime import date


#   ===================chrome==============

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.managed_default_content_settings.images": 2,'profile.managed_default_content_settings.javascript': 2}
    chromeOptions.binary_location = '/usr/bin/google-chrome'
    chromeOptions.add_experimental_option("prefs",prefs)    
    
#     ====================Firefox====================
    firefox_profile = webdriver.FirefoxProfile()
    options = Options()
    options.headless = True
  
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.CSS", 2)  ## CSS
    firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.Cookies", 2)  ## Cookies
    firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.Flash", 2)  ## Flash
    firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.Java", 2)  ## Java
    firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.JavaScript", 2)  ## JavaScript
    firefox_profile.set_preference("thatoneguydotnet.QuickJava.startupStatus.Silverlight", 2)  ## Silverlight
    firefox_profile.set_preference('browser.migration.version', 9001)
    firefox_profile.set_preference('permissions.default.stylesheet', 2)
    ## Disable images
    firefox_profile.set_preference('permissions.default.image', 2)
    ## Disable Flash
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
                                  'false')
    driver = webdriver.Firefox(options=options,executable_path=os.getcwd() +'/geckodriver',firefox_profile=firefox_profile)
    

   
