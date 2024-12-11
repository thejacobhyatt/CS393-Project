import pandas as pd
import numpy as np

# Sample data for other dataframes

statuses = pd.read_csv('status.csv')
departments = pd.read_csv('departments.csv')
advisors = pd.read_csv('advisors.csv')
researchers = pd.read_csv('researchers.csv')
sponsors = pd.read_csv('sponsors.csv')
projects = pd.read_csv('random_titles.csv')


# Function to randomly select rows from dataframes
def randomly_select(df, n):
    return df.sample(n=n, replace=True).reset_index(drop=True)

# Number of rows for the final dataset
n_rows = 10

# Create the final dataset
final_data = pd.DataFrame({
    'title': randomly_select(projects, n_rows)['title'],
    'biography': randomly_select(projects, n_rows)['biography'],
    'status': randomly_select(statuses, n_rows)['status_name'],
    'department_name': randomly_select(departments, n_rows)['department_name'],
    'advisors': randomly_select(advisors, n_rows)['first_name'],
    'researchers': randomly_select(researchers, n_rows)['name'],
    'sponsors': randomly_select(sponsors, n_rows)['name'],
})

print(final_data)
final_data.to_csv('projects.csv', index=False)