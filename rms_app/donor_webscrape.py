import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Send an HTTP request to the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_wealthiest_charitable_foundations'  
response = requests.get(url)

# Step 2: Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Find the table on the page (assuming it's the first table)
table = soup.find('table', {'class': 'wikitable'})

# Step 4: Extract table headers
headers = []
for th in table.find_all('th'):
    headers.append(th.get_text(strip=True))

# Step 5: Extract table rows
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    cols = row.find_all('td')
    cols = [col.get_text(strip=True) for col in cols]
    rows.append(cols)

# Step 6: Create a DataFrame using the extracted data
df = pd.DataFrame(rows, columns=headers)

# Step 7: Display the DataFrame or save it to a file
print(df)

# Optional: Save the data to a CSV file
df.to_csv('donor_table.csv', index=False)
