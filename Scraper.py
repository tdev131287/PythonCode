from selenium import webdriver
import time
import os
import pandas as pd
import time

def GetLinks():

    dfLinks = pd.DataFrame()
    driver = webdriver.Chrome()
    # url="https://ensun.io/search?threshold=VERY_LOW&continents=EUROPE&q=Battery%20management%20and%20analytics%20software&minEmployees=51&maxEmployees=5000&industries=IT%2C%20Software%20and%20Services&industries=Oil%2C%20Energy%20and%20Gas&industries=Utilities&categories=SERVICE_PROVIDER"
    for pg in range(0,32):
        url ='https://www.csiaexchange.com/common/default.aspx?id=4&pi='+str(pg)+'&salt=69249&ps=100'
        # url="https://www.csiaexchange.com/common/default.aspx?id="+str(pg)+"&pi=0&salt=69249&ps=100"
        
        driver.get(url)
        print('Running page count - '+str(pg))
        # import ipdb;ipdb.set_trace()
        itemList = driver.find_elements_by_css_selector("[class='list-items']")[0]
        ulItems = itemList.find_elements_by_tag_name('ul')[0]
        itm=ulItems.find_elements_by_tag_name('li')[0]
        for itm in ulItems.find_elements_by_tag_name('li'):
            
            try:
                nextLink = itm.find_elements_by_tag_name('a')[1].get_attribute('href')
            except:
                nextLink='NA'
            # import ipdb;ipdb.set_trace()
            dfLinks = dfLinks.append({'NextLink':nextLink,'Source':url},ignore_index=True)
            # dfAll = dfAll.append({'Catefory':category,'BasicInfo':info,'Details':desc,'MetaInfo':metaInfo,'Link':url},ignore_index=True)
            dfLinks.to_excel('LinksResult.xlsx',index=False)
def DetailsInfo():
    dfAllInfo = pd.DataFrame()
    dflinks = pd.read_excel('LinksResult.xlsx')
    driver = webdriver.Chrome()
    for idx in range(len(dflinks)):
        url = dflinks.iloc[idx]['NextLink']
        # url='https://www.csiaexchange.com/2214/Data-Science-Automation'
        
        driver.get(url)
        time.sleep(10)
        basicInfo = driver.find_elements_by_css_selector("[class='topMainInfo white-well']")[0]
        name = basicInfo.find_elements_by_css_selector("[class='name']")[0].text
        type = basicInfo.find_elements_by_css_selector("[class='categSpan']")[0].text
        add = basicInfo.find_elements_by_css_selector("[class='topInfoDetails col-xs-12 col-sm-6 ']")[0].text
        contactInfo =basicInfo.find_elements_by_css_selector("[class='infromationTable']")[0].text
        email=basicInfo.find_elements_by_css_selector("[class='infromationTable emailsDetail']")[0].text
        # import ipdb;ipdb.set_trace()
        try:
            foundedYear = basicInfo.find_elements_by_css_selector("[class='value estYear']")[0].text
        except:
            pass
        linkedin =basicInfo.find_elements_by_css_selector("[class='social linkedin']")[0].get_attribute('href')
        try:
            branchlist = driver.find_elements_by_css_selector("[class='branches__container']")[0]
            Allbranch=''
            for branch in branchlist.find_elements_by_css_selector("[class='branch']"):
                # right__info
                if Allbranch=='':
                    Allbranch = branch.text
                else:
                    Allbranch= Allbranch +'|'+ branch.text
        except:
            Allbranch='NA'
            
        # categoriesOrganization compactBox hideOnEmpty
        try:
            Industries = driver.find_elements_by_css_selector("[class='categoriesOrganization compactBox hideOnEmpty']")[0].text
        except:
            Industries='NA'
        try:
            Specialties = driver.find_elements_by_css_selector("[class='categoriesOrganization compactBox hideOnEmpty']")[1].text
        except:
            Specialties='NA'
        try:
            Products = driver.find_elements_by_css_selector("[class='categoriesOrganization compactBox hideOnEmpty']")[2].text
        except:
            Products='NA'
        try:
            Certifications=driver.find_elements_by_css_selector("[class='categoriesOrganization compactBox hideOnEmpty']")[3].text
        except:
            Certifications='NA'
        try:
            Service  =driver.find_elements_by_css_selector("[class='categoriesOrganization compactBox hideOnEmpty']")[4].text
        except:
            Service='NA'

        dfAllInfo = dfAllInfo.append({'Name':name,'Type':type,'Address':add,'Contact':contactInfo,'E-Mail':email,'FYear':foundedYear,'Linkedin':linkedin,'Branch':Allbranch,
                                    'Industries':Industries,'Specialties':Specialties,'Products':Products,'Certifications':Certifications,'Service':Service,'Source':url},ignore_index=True)
        
        dfAllInfo.to_excel('AllResult.xlsx',index=False)

    # categoriesOrganization compactBox hideOnEmpty

if __name__=="__main__":
    # GetLinks()
    DetailsInfo()