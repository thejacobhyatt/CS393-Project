from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True)
    status_color = models.CharField(max_length=6)

    def __str__(self):
        return self.status_name

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_head = models.CharField(max_length=50)
    department_loc = models.CharField(max_length=6)
    department_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.department_name}"

class Advisor(models.Model):
    advisor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Researcher(models.Model):
    researcher_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Sponsor(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    amount_donated = models.IntegerField()
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class ResearchProject(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    start_date = models.DateTimeField(auto_now_add=True)
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    advisors = models.ManyToManyField(Advisor, related_name="research_projects")
    researchers = models.ManyToManyField(Researcher, related_name="research_projects")
    sponsors = models.ManyToManyField(Sponsor, related_name="research_projects")

    def __str__(self):
        return self.title
