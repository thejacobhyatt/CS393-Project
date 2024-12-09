import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates'  
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'class': 'wikitable'})

headers = ['Year']
for th in table.find_all('th')[1:7]:
    headers.append(th.get_text(strip=True))

rows = []
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')[:6] 
    if cols:
        year = row.find('th').get_text(strip=True)  
        cols_text = [year] + [col.get_text(strip=True) for col in cols]  
        rows.append(cols_text)

df = pd.DataFrame(rows, columns=headers)

df['Year'] = df['Year'].astype(int)
df = df[df['Year'] >= 2000]
df['Economics'] = df['Prize in Economic Sciences[13][a]']
df['Medicine'] = df["Physiologyor Medicine"]
df = df.drop(columns=['Prize in Economic Sciences[13][a]',"Physiologyor Medicine"])

records = []

for index, row in df.iterrows():
    for department in ['Physics', 'Chemistry', 'Literature', 'Peace', 'Economics', 'Medicine']:
        first_name = row[department].split(';')[0].strip()
        records.append({'Name': first_name, 'Year': row['Year'], 'Department': department})

df_names = pd.DataFrame(records)
df_names.to_csv('researcher.csv', index=False)
