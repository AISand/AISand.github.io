import requests
from bs4 import BeautifulSoup
from csv import writer
import os
import pandas as pd

LogsList = open('logs.txt')
Log_i = LogsList.readlines()

for line in Log_i:

    url = 'https://logs.tf/{}'.format(int(line))
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'lxml')
    MatchTitle = soup.find('h3', id='log-name').string

    with open('{}.csv'.format(int(line)), 'w', encoding='utf8', newline='') as f:

        # Header
        table_headers = []
        Writer = writer(f)
        for i in soup.find_all('th')[1:17]:
            title = i.text
            table_headers.append(title)
        table_headers.append('RO')
        Writer.writerow(table_headers)

        Table = soup.find('table', class_='table log')
        BS = soup.find('div', class_='score blu')
        RS = soup.find('div', class_='score red')
        # Stats

        BScore = int(BS.find('h1', class_='pull-right').text)
        RScore = int(RS.find('h1', class_='pull-left').text)
        TScore = BScore + RScore

        for j in Table.find_all('tr')[1:]:
            Name = j.find('li', role='menuitem').contents[0].attrs['href'][9:]
            C = j.find('i').attrs['class'][1]
            Stats = j.find_all('td')
            K = Stats[3].string
            A = Stats[4].string
            D = Stats[5].string
            DA = Stats[6].string
            DAM = Stats[7].string
            KAD = Stats[8].string
            KD = Stats[9].string
            DT = Stats[10].string
            DTM = Stats[11].string
            HP = Stats[12].string
            BS = Stats[13].string
            HS = Stats[14].string
            AS = Stats[15].string
            CAP = Stats[16].string

            info = [Name, C, K, A, D, DA, DAM, KAD, KD, DT, DTM, HP, BS, HS, AS, CAP, TScore]
            Writer.writerow(info)

# Combine

master_df = pd.DataFrame()

for file in os.listdir(os.getcwd()):
    if file.endswith('.csv'):
        master_df = master_df.append(pd.read_csv(file))

d = {'K': 'sum', 'A': 'sum', 'D': 'sum', 'DA': 'sum', 'DA/M': 'mean', 'KA/D': 'mean', 'K/D': 'mean', 'DT': 'sum',
     'DT/M': 'mean', 'HP': 'sum', 'BS': 'sum', 'HS': 'sum', 'AS': 'sum', 'CAP': 'sum'}
df_new = master_df.groupby('Name', as_index=False).aggregate(d).reindex(columns=master_df.columns)

Username = []
for x in df_new['Name']:
    RGL_url = 'https://rgl.gg/Public/PlayerProfile.aspx?p={}'.format(x)
    RGL_page = requests.get(RGL_url)
    RGL_soup = BeautifulSoup(RGL_page.content, 'lxml')
    Name2 = RGL_soup.find_all('span', id='ContentPlaceHolder1_Main_lblPlayerName')[0].text
    Username.append(Name2)

df_new['Name'] = Username

df_new.to_csv('C:\\Users\\Aidan\\Desktop\\py\\logscombiner\\Masterlog\\Masterlog.csv', index=False)
