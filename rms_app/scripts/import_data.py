import pandas as pd
from rms_app.models import Status, Department, Advisor, Researcher, Sponsor, ResearchProject
from django.contrib.auth.models import User

# Import data for Status
status_csv_path = 'rms_app/data/status.csv'
status_df = pd.read_csv(status_csv_path)

for index, row in status_df.iterrows():
    status, created = Status.objects.get_or_create(
        status_name=row['status_name'],
        defaults={
            'status_color': row['status_color'],
        }
    )
    print(f"{'Created' if created else 'Found'} Status: {status.status_name}")

# Import data for Department
department_csv_path = 'rms_app/data/departments.csv'
department_df = pd.read_csv(department_csv_path)

for index, row in department_df.iterrows():
    department, created = Department.objects.get_or_create(
        department_head=row['department_head'],
        department_loc=row['department_loc'],
        department_name=row['department_name'],

    )
    print(f"{'Created' if created else 'Found'} Department: {department}")

# Import data for Advisors
advisor_csv_path = 'rms_app/data/advisors.csv'
advisor_df = pd.read_csv(advisor_csv_path)

for index, row in advisor_df.iterrows():
    user = User.objects.filter(username=row['first_name']).first()
    advisor, created = Advisor.objects.get_or_create(
        email=row['email'],
        defaults={
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'user': user,
        }
    )
    print(f"{'Created' if created else 'Found'} Advisor: {advisor}")

# Import data for Researchers
researcher_csv_path = 'rms_app/data/researchers.csv'
researcher_df = pd.read_csv(researcher_csv_path)

for index, row in researcher_df.iterrows():
    user = User.objects.filter(username=row['first_name']).first()
    researcher, created = Researcher.objects.get_or_create(
        email=row['email'],
        defaults={
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'phone': row['phone'],
            'user': user,
        }
    )
    print(f"{'Created' if created else 'Found'} Researcher: {researcher}")

# Import data for Sponsors
sponsor_csv_path = 'rms_app/data/sponsors.csv'
sponsor_df = pd.read_csv(sponsor_csv_path)

for index, row in sponsor_df.iterrows():
    user = User.objects.filter(username=row['name']).first()
    sponsor, created = Sponsor.objects.get_or_create(
        email=row['email'],
        defaults={
            'name': row['name'],
            'phone': row['phone'],
            'amount_donated': row['amount_donated'],
        }
    )
    print(f"{'Created' if created else 'Found'} Sponsor: {sponsor}")

# Import data for Research Projects
project_csv_path = 'rms_app/data/projects.csv'
project_df = pd.read_csv(project_csv_path)

for index, row in project_df.iterrows():
    status = Status.objects.get(status_name=row['status'])
    department = Department.objects.get(department_name=row['department_name'])

    project, created = ResearchProject.objects.get_or_create(
        title=row['title'],
        defaults={
            'biography': row['biography'],
            'status': status,
            'department': department,
        }
    )

    # Link advisors
    advisor = Advisor.objects.get(first_name=row['advisors'])
    project.advisors.add(advisor)

    # Link researchers
    for researcher_name in row['researchers'].split(';'):
        researcher = Researcher.objects.get(first_name=researcher_name.split()[0], last_name=researcher_name.split()[1])
        project.researchers.add(researcher)

    # Link sponsors
    for sponsor_name in row['sponsors'].split(';'):
        sponsor = Sponsor.objects.get(name=sponsor_name)
        project.sponsors.add(sponsor)

    print(f"{'Created' if created else 'Found'} Research Project: {project.title}")

print("CSV data has been successfully loaded into the Django database.")