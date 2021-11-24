import pandas as pd
import glob
import os

    folderName=os.getcwd() +  '/downloaded data/all'+ '/'
    all_data = pd.DataFrame()
    directory=folderName
  
    files=glob.glob(folderName+'*.xls*')
    r=1
    for filename in files:
        print(os.path.join(os.path.dirname(__file__))+ filename)
       
        attachment= filename
    #    print(attachment)
        df = pd.read_excel(attachment)
        # df.columns = map(lambda x: x.upper(),df.columns)
    #    print(df)
        all_data = all_data.append(df)
        r=r+1
        print(r)
    
    
