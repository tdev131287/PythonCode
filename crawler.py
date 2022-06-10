import tabula
import pandas as pd
import requests
import os

def fetchtable():

    look_up = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
            'June': 6, 'Jun': 6,'Jul': 7,'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


    all_data=pd.DataFrame()



    # url=  'https://www.fao.org/3/cb8263en/cb8263en.pdf'
    #
    #
    #
    # r=requests.get(url).content
    path=os.path.join(os.path.dirname(__file__))+ "/downloaded files/data.pdf"
    #
    #
    # with open(path, 'wb') as f:
    #     f.write(r)



    # table = tabula.read_pdf(path,pages=3,pandas_options={'header': None})

    table = tabula.read_pdf(path,pages=3)

    df=table[2]
    df.columns = df.iloc[0]
    import ipdb; ipdb.set_trace()

    for rowloop in range(0,len(df)):
       if df.iloc[rowloop,0]=="Monthly":

           startrow=rowloop
           break;

    df=df[startrow+1:]
    df.columns=["Date","Oilseeds","Vegetable oils","Oilcakes"]
    # print(df)

    columns = list(df)
    for x in range(1,len(columns)):
        cols = [0,x]
        df1 = df[df.columns[cols]]
        df1['commodity_name_source']=str(columns[x])
        df1.columns=["Date","value","commodity_name_source"]
        all_data = all_data.append(df1)

    dfall=all_data[all_data['value'].notnull()]
    new  = dfall['Date'].str.split(" - ", n = 1, expand = True)
    dfall['Month'] = new[1]
    dfall['Year'] =new[0]

    dfall['Month'] = dfall['Month'].apply(lambda x: look_up[x])

    mapinig=pd.read_excel(os.path.join(os.path.dirname(__file__))+ "/mapping.xlsx")

    dfall=dfall.groupby(['Year','Month','commodity_name_source'], as_index=False)['value'].mean()

    dfall['Day']=1
    dfall['timeframe_monthly'] =pd.to_datetime(dfall[['Year', 'Month', 'Day']])
    dfall = dfall.sort_values(by=['commodity_name_source','timeframe_monthly'], ascending=[True,False])

    dfall['timeframe_monthly'] = dfall['timeframe_monthly'].dt.strftime('%b-%Y')

    dfall=dfall.merge(mapinig,on='commodity_name_source')

    dfall['db_id']=""

    dfall['is_approved']=''


    dfall = dfall[["db_id", "source_ref", "commodity_name", "commodity_group", "commodity_grade", "commodity_subgrade", "geography", "unit", "timeframe_monthly", "value" , "is_approved"]]

    dfall.to_excel("finalData.xlsx",index=False)

if __name__ == '__main__':

    fetchtable()
