import requests
from bs4 import BeautifulSoup
import pandas as pd

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
df.to_csv("largest_companies_by_revenue.csv", index=False)