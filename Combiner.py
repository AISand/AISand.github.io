import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Combine

master_df = pd.DataFrame()

for file in os.listdir(os.getcwd()):
    if file.endswith('.csv'):
        master_df = master_df.append(pd.read_csv(file))

d = {'C': 'last', 'K': 'sum', 'A': 'sum', 'D': 'sum', 'DA': 'sum', 'DA/M': 'mean', 'KA/D': 'mean', 'K/D': 'mean', 'DT': 'sum', 'DT/M': 'mean', 'HP': 'sum', 'BS': 'sum', 'HS': 'sum', 'AS': 'sum', 'CAP': 'sum', 'RO': 'sum'}
df_new = master_df.groupby('Name', as_index=False).aggregate(d).reindex(columns=master_df.columns)

Username = []
for x in df_new['Name']:
    RGL_url = 'https://rgl.gg/Public/PlayerProfile.aspx?p={}'.format(x)
    RGL_page = requests.get(RGL_url)
    RGL_soup = BeautifulSoup(RGL_page.content, 'lxml')
    Name2 = RGL_soup.find_all('span', id='ContentPlaceHolder1_Main_lblPlayerName')[0].text
    Username.append(Name2)

df_new['Name'] = Username

#df1 = df_new.where(pd.notnull(df_new), '0')

df_new.to_csv('C:\\Users\\Aidan\\Desktop\\py\\logscombiner\\Masterlog\\Masterlog.csv', index=False)

