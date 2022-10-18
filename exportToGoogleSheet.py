import requests
import json
import pandas as pd
import os
import datetime
from dateutil.relativedelta import relativedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import numpy as np
import time

def exportToGoogleSheet():

    ######uploading commodity row datat###################
    dfall=pd.read_excel('D:/Diwaker-Data/JSON-Automation/Commodity data.xlsx')
    # dfall = dfall.replace(np.nan, '', regex=True)

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('D:/Diwaker-Data/JSON-Automation/sanofidataupdate-a43b7deb0ffc.json', scope)

    # write df to google sheet
    # spreadsheet_key = '1aKMEFfJEYTtToB-5PpW8ADat2FGAIVi-6tJA5A7zGiw'
    spreadsheet_key = '1D2HVK1ZCItCme4y5AC1rP_OwLBP1znCxxrPPALmhFWY'
    wks_name = 'Sheet1'
    d2g.upload(dfall, spreadsheet_key, wks_name, credentials=creds, row_names=False)


if __name__=="__main__":

    exportToGoogleSheet()
