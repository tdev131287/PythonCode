# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:47:10 2020

@author: Devendra.Tripathi
"""
from xml.dom import minidom
import requests
import os
import xml.etree.ElementTree as ET
import pandas as pd
import re
import datetime
# from sqlalchemy import create_engine
import pandas.io.sql as psql
import datetime
import time
from goose3 import Goose
import os
def getCommodityNews(url,cname):

    active_path=os.path.join(os.path.dirname(__file__))
    mstdf = pd.DataFrame(columns=['SourceUrl','Commodity','Title', 'Link', 'CommodityName','ReportDate','Description','Source','NewsTitle','Contents'])

    now= datetime.datetime.now()
    xdate =str(now.year) + '-' + str('{:02d}'.format(now.month)) +'-'+ str('{:02d}'.format(now.day))

    folderName=os.path.join(os.path.dirname(__file__)) + '/' + xdate + '/'

    if not os.path.exists(folderName):
        os.mkdir(folderName)

#    import ipdb;ipdb.set_trace()
    r = requests.get(url,verify=False)

    TAG_RE = re.compile(r'<[^>]+>')
    with open(active_path+ "/rawdata.xml", 'wb') as f:
        f.write(r.content)
#    mydoc = minidom.parse(active_path + '/rawdata.xml')
    # import ipdb; ipdb.set_trace()
    mytree = ET.parse(active_path + '/rawdata.xml')

    myroot = mytree.getroot()
    vguid =myroot[0].find('title').text.replace('"" - Google News','').replace('""','')
#    print(myroot[0].tag)
    try:
        for x in myroot[0].findall('item'):
    #     print(x.tag, x.attrib)
            vxtitle =x.find('title').text
            vlink =x.find('link').text

    #        vguid =x.find('guid isPermaLink').text

            vpubDate =x.find('pubDate').text.replace(" GMT","")

            vdescription =x.find('description').text
            vdescription=TAG_RE.sub('', vdescription)
            vdescription=vdescription.replace('&nbsp;',' ')
            vsource =x.find('source').text
    #        print('Before')
    #        print(vlink)
            resp=extractArticle(vlink)

    #        vtitle=resp['title'].encode("utf8","ignore")
    #        vtitle=vtitle.replace("b'",'')
    #        vContents=resp['content'].encode("utf8","ignore")




            mstdf = mstdf.append({'SourceUrl':url,'Commodity':cname,'Title': vxtitle, 'Link': vlink, 'CommodityName': vguid,'ReportDate'
                                  : vpubDate,'Description': vdescription,'Source': vsource
                                  ,'NewsTitle':resp['title'].encode("utf8","ignore"),'Contents':resp['content'].encode("utf8","ignore")}, ignore_index=True)

#        print('After')
#    Wed, 26 Feb 2020 03:52:00 GMT
        mstdf['ReportDate'] = mstdf['ReportDate'].apply(lambda x: datetime.datetime.strptime(x,'%a, %d %b %Y %H:%M:%S'))
        mstdf['ReportDate'] = mstdf['ReportDate'].dt.strftime('%m/%d/%Y')

        mstdf=mstdf.sort_values(by=['ReportDate'], ascending=[False])

        # import ipdb;ipdb.set_trace()
        mstdf.to_csv(folderName+'/CompiledCommodity'+'_'+xdate+'.csv',mode='a', header=False,index=False)
    except:
        pass
#    print('Create a cvs file')
    # agdf = pd.read_csv(folderName+'/'+cname+'_News_'+xdate+'.csv',index_col=0,converters={'ReportDate':pd.to_datetime })
    # agdf.to_csv('compiwszledCommodity.csv')
    # agdf.to_sql('dy_commoditynews', con = engine, if_exists = 'append', chunksize = 1000)

def extractArticle(hurl):
        try:
            print(hurl)
            article = g.extract(url=hurl)
            if article.cleaned_text == "" or article.cleaned_text == None:
                    desc = v2.extract(hurl)
                    msg = {"title":article.title,"content": desc}
            else:
                    msg = {"title":article.title,"content": article.cleaned_text}
            return msg
        except:
            msg = {"title":'No Data Found',"content":'No Data Found'}
#                print (traceback.format_exc())
            return msg

def ReviewDate():
    mstdf = pd.read_excel('Reveiw.xlsx')

    mstdf['Date'] = mstdf['Date'].apply(lambda x: datetime.datetime.strptime(x,'%a, %d %b %Y %H:%M:%S'))
    mstdf['Date'] = mstdf['Date'].dt.strftime('%m/%d/%Y')
    mstdf=mstdf.sort_values(by=['Date'], ascending=[False])
    mstdf.to_excel('ReviewDate.xlsx')



def Title_Count_Review():
    active_path=os.path.join(os.path.dirname(__file__))
    url='https://news.google.com/rss/search?q=%22crude%20oil%22&hl=en-IN&gl=IN&ceid=IN:en&pubDate'
    cname ='Crude_oil'
    r = requests.get(url)
    mstdf = pd.DataFrame(columns=['Title', 'Date','Link'])
    TAG_RE = re.compile(r'<[^>]+>')
    with open(active_path+ "/rawdata.xml", 'wb') as f:
        f.write(r.content)
#    mydoc = minidom.parse(active_path + '/rawdata.xml')
    mytree = ET.parse(active_path + '/rawdata.xml')
    myroot = mytree.getroot()
    vguid =myroot[0].find('title').text.replace('"" - Google News','').replace('""','')
#    print(myroot[0].tag)

    for x in myroot[0].findall('item'):
#     print(x.tag, x.attrib)
        vxtitle =x.find('title').text
        vpubDate =x.find('pubDate').text
        vlink =x.find('link').text
        mstdf = mstdf.append({'Title': vxtitle, 'Date': vpubDate,'Link':vlink},ignore_index=True)
    mstdf.to_excel('testV1.xlsx')
def Insert_in_DB():

    engine = create_engine("mysql+pymysql://{user}:{pw}@172.24.33.22/{db}"
                       .format(user="root",
                               pw="Sc@1234",
                               db="commoditynews"))
    df = pd.read_csv('Crude_oil_News_2020-02-28.csv',converters={'Date':pd.to_datetime })

#    df['Date']= pd.to_datetime(df['Date'])

    print(df.info())

    df.to_sql('dy_commoditynews', con = engine, if_exists = 'append', chunksize = 1000)
#    df.to_sql('dy_commoditynews', con = engine,if_exists = 'append')


if __name__=="__main__":
    g=Goose()
    active_path=os.path.join(os.path.dirname(__file__))
    df = pd.read_excel(active_path+'/Google News.xlsx')

    for xrow in range(len(df)):
        xurl = df.iloc[xrow]['API to be used by Macro']
        flname = df.iloc[xrow]['Keyword']
        print('Running Commodity - >' + str(flname))
        getCommodityNews(xurl,flname)

#    Title_Count_Review()
#    ReviewDate()
#    Insert_in_DB()
#
