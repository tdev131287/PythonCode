import pandas as pd
import glob
import os

folderName=os.path.join(os.path.dirname(__file__)) + '/' + 'Downloaded files'+ '/'
all_data = pd.DataFrame()
directory=folderName
os.chdir(directory)
files=glob.glob('*.xls*')
r=1
for filename in files:
    print(os.path.join(os.path.dirname(__file__))+ filename)
    attachment=folderName + filename
#    print(attachment)
    df = pd.read_excel(attachment)
#    print(df)
    all_data = all_data.append(df)
    r=r+1
    print(r)
    
    
all_data.to_excel(os.path.join(os.path.dirname(__file__)) + '/' + 'Final_file.xlsx')
    
    