
import pandas as pd
#import calender
import datetime


#03. February 2020

#https://www.journaldev.com/23365/python-string-to-datetime-strptime


df=pd.read_excel("test.xlsx")

def mapper(month):
    return datetime.datetime.strptime(month,'%d. %B %Y')
#   return month.strptime('%d. %B %Y') 

def mapper1(month):
   return month + 'dddddddd'

df['Date1'] = df['Month_Code1'].apply(mapper)
df['Date'] = df['Month_Code1'].apply(lambda x: datetime.datetime.strptime(x,'%d. %B %Y'))
df['col1'] = df['String123'].apply(mapper1)
df.to_excel('test1.xlsx')
print(df)


