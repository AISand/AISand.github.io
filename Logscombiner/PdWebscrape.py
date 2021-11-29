import requests
from bs4 import BeautifulSoup
import pandas as pd

LogsList = open('logs.txt')
Log_i = LogsList.readlines()

df = pd.DataFrame()

for line in Log_i:

    url = 'https://logs.tf/{}'.format(int(line))
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'lxml')
    Table = soup.find('table', class_='table log')

    # Round Counter
    BS = soup.find('div', class_='score blu')
    RS = soup.find('div', class_='score red')
    BScore = int(BS.find('h1', class_='pull-right').text)
    RScore = int(RS.find('h1', class_='pull-left').text)
    TScore = BScore + RScore

    # Stats

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

        KR = int(K)/int(TScore)
        AR = int(A)/int(TScore)
        DR = int(D)/int(TScore)
        BSR = int(BS)/int(TScore)
        HSR = int(HS)/int(TScore)

        d = {'Name': [Name], 'C': [C], 'K': [int(K)], 'K/R': [float(KR)], 'A': [int(A)], 'A/R': [float(AR)], 'D': [int(D)], 'D/R': [float(DR)], 'DA': [int(DA)], 'DA/M': [float(DAM)], 'KA/D': [float(KAD)], 'K/D': [float(KD)], 'DT': [int(DT)], 'DT/M': [float(DTM)], 'HP': [int(HP)], 'BS': [int(BS)], 'BS/R': [float(BSR)], 'HS': [int(HS)], 'HS/R': [float(HSR)], 'AS': [int(AS)], 'CAP': [int(CAP)], 'RO': [int(TScore)]}

        df = df.append(pd.DataFrame(data=d))

# Combine dataframe sorted by similar playerID

d = {'C': 'last', 'K': 'sum', 'K/R': 'mean', 'A': 'sum', 'A/R': 'mean', 'D': 'sum', 'D/R': 'mean', 'DA': 'sum', 'DA/M': 'mean', 'KA/D': 'mean', 'K/D': 'mean', 'DT': 'sum', 'DT/M': 'mean', 'HP': 'sum', 'BS': 'sum', 'BS/R': 'mean', 'HS': 'sum', 'HS/R': 'mean', 'AS': 'sum', 'CAP': 'sum', 'RO': 'sum'}
df_new = df.groupby('Name', as_index=False).aggregate(d).reindex(columns=df.columns)

print('Logs combined')

# Username Convert to RGL Alias

Username = []
for x in df_new['Name']:
    RGL_url = 'https://rgl.gg/Public/PlayerProfile.aspx?p={}'.format(x)
    RGL_page = requests.get(RGL_url)
    RGL_soup = BeautifulSoup(RGL_page.content, 'lxml')
    Name2 = RGL_soup.find_all('span', id='ContentPlaceHolder1_Main_lblPlayerName')[0].text
    Username.append(Name2)
    print(Name2)

df_new['Name'] = Username

df1 = df_new.where(pd.notnull(df_new), '0')

#Write to csv

df_new.to_csv('C:\\Users\\Aidan\\Desktop\\py\\logscombiner\\Masterlog\\Masterlog.csv', index=False)