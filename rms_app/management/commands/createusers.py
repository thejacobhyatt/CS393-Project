# create_groups.py

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from rms_app.models import Advisor

class Command(BaseCommand):
    def handle(self, **options):
        groups = ['Researcher', 'Advisors']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
        
        try:
            Advisor = User.objects.get(username='advisor')
        except User.DoesNotExist:
            AdvisorUser = User.objects.create_user('advisor', 'advisor@example.com', 'advisorpassword')
            AdvisorUser.first_name = 'Shane'
            AdvisorUser.last_name = 'Reeves'
            AdvisorGroup = Group.objects.get(name='Advisors')
            AdvisorUser.groups.add(AdvisorGroup)
            AdvisorUser.save()

        try:
            Advisor = Advisor.objects.get(first_name="Shane", last_name="Reeves")
        except Advisor.DoesNotExist:
            Advisor = Advisor.objects.create(first_name="Shane", last_name="Reeves", department="EECS", user=AdvisorUser)
            Advisor.save()