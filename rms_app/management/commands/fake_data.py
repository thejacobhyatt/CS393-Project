import random
from django.core.management.base import BaseCommand
from faker import Faker
from rms_app.models import Status, Department, Advisor, Researcher, Sponsor, ResearchProject

fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **kwargs):
        # Create fake Status entries
        for _ in range(3):
            status = Status.objects.create(
                status_name=self.status_word(),
                status_color=fake.hex_color()[1:]  # Remove the '#' from the hex color
            )

        # Create fake Department entries
        for _ in range(3):
            department = Department.objects.create(
                department_head=fake.name(),
                department_loc=fake.state_abbr()
            )

        # Create fake Advisor entries
        for _ in range(3):
            advisor = Advisor.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )

        # Create fake Researcher entries
        for _ in range(3):
            researcher = Researcher.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=self.generate_fake_phone_number()  # Use the custom phone number generator
            )

        # Create fake Sponsor entries
        for _ in range(3):
            sponsor = Sponsor.objects.create(
                name=fake.company(),
                email=fake.email(),
                phone=self.generate_fake_phone_number(),  # Use the custom phone number generator
                amount_donated=random.randint(1000, 1000000)
            )

        # Create fake ResearchProject entries
        for _ in range(3):
            status = Status.objects.all().order_by('?').first()
            department = Department.objects.all().order_by('?').first()

            project = ResearchProject.objects.create(
                title=fake.sentence(nb_words=6),
                biography=fake.text(),
                status=status,
                department=department,
                start_date=fake.date_time_this_year()
            )

            # Add random Advisors to the project
            advisors = Advisor.objects.all()
            project.advisors.add(*random.sample(list(advisors), 2))  # Randomly assign 2 advisors

            # Add random Researchers to the project
            researchers = Researcher.objects.all()
            project.researchers.add(*random.sample(list(researchers), 2))  # Randomly assign 2 researchers

            # Add random Sponsors to the project
            sponsors = Sponsor.objects.all()
            project.sponsors.add(*random.sample(list(sponsors), 2))  # Randomly assign 2 sponsors

        self.stdout.write(self.style.SUCCESS('Database populated with fake data!'))

    def generate_fake_phone_number(self):
        # Generate a 12-digit phone number
        return str(random.randint(100000000000, 999999999999))  # 12 digits
    
    def status_word(self):
        status_type = ['Completed', 'In Progress', 'Not Started']
        return random.choice(status_type)
