from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from rms_app.models import Advisor, Researcher

class Command(BaseCommand):
    def handle(self, **options):
        # Create groups
        groups = ['Researcher', 'Advisors']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Group '{group_name}' created successfully.")
            else:
                self.stdout.write(f"Group '{group_name}' already exists.")

        # Create the advisor user if it does not exist
        try:
            advisor_user = User.objects.get(username='advisor')
            self.stdout.write("Advisor user already exists.")
        except User.DoesNotExist:
            advisor_user = User.objects.create_user('advisor', 'advisor@example.com', 'advisorpassword')
            advisor_user.first_name = 'Shane'
            advisor_user.last_name = 'Reeves'
            advisor_group = Group.objects.get(name='Advisors')
            advisor_user.groups.add(advisor_group)
            advisor_user.save()
            self.stdout.write("Advisor user created successfully.")

        # Create the advisor record if it does not exist
        try:
            advisor = Advisor.objects.get(first_name="Shane", last_name="Reeves")
            self.stdout.write("Advisor record already exists.")
        except Advisor.DoesNotExist:
            advisor = Advisor.objects.create(
                first_name="Shane",
                last_name="Reeves",
                email="advisor@example.com",  # Adjust as necessary
                user=advisor_user
            )
            self.stdout.write("Advisor record created successfully.")

        # Create the researcher user if it does not exist
        try:
            researcher_user = User.objects.get(username='researcher')
            self.stdout.write("Researcher user already exists.")
        except User.DoesNotExist:
            researcher_user = User.objects.create_user('researcher', 'researcher@example.com', 'researcherpassword')
            researcher_user.first_name = 'Alex'
            researcher_user.last_name = 'Johnson'
            researcher_group = Group.objects.get(name='Researcher')
            researcher_user.groups.add(researcher_group)
            researcher_user.save()
            self.stdout.write("Researcher user created successfully.")

        # Create the researcher record if it does not exist
        try:
            researcher = Researcher.objects.get(first_name="Alex", last_name="Johnson")
            self.stdout.write("Researcher record already exists.")
        except Researcher.DoesNotExist:
            researcher = Researcher.objects.create(
                first_name="Alex",
                last_name="Johnson",
                email="researcher@example.com",  # Adjust as necessary
                user=researcher_user
            )
            self.stdout.write("Researcher record created successfully.")

        self.stdout.write("Advisor and Researcher user creation completed successfully.")
