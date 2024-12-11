import requests
from bs4 import BeautifulSoup
import pandas as pd
import random


url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", {"class": "wikitable"})

headers = [header.text.strip() for header in table.find_all("th")]

rows = []
for row in table.find_all("tr")[1:]:  # Skip the header row
    cells = [cell.text.strip() for cell in row.find_all(["td", "th"])]
    rows.append(cells)

df = pd.DataFrame(rows, columns=headers)

df['phone'] = [f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}" for _ in range(len(df))]
df['email'] = ['admin@' + name.replace(' ', '').lower() + '.com' for name in df['Name']]
df = df.rename(columns={
    'Name': 'name',
    'Revenue (USD millions)' : 'amount_donated'
})
df['amount_donated'] = df['amount_donated'].str.replace(',', '').astype(int)
df = df.drop(columns=['Industry', 'Rank','Employees', 'Headquarters', 'Revenue growth'])

df.to_csv("sponsors.csv", index=False)