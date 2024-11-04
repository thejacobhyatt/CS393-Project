from django.db import models
from django.contrib.auth import get_user_model

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50)
    status_color = models.CharField(max_length=6)

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_head = models.CharField(max_length=50)
    department_loc = models.CharField(max_length=6)

class Advisor(models.Model):
    advisor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

class Researcher(models.Model):
    researcher_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)  

class Sponsor(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)  
    amount_donated = models.IntegerField()


class ResearchProject(models.Model):
    project_id = models.AutoField(primary_key=True, verbose_name="Project ID")
    title = models.CharField(max_length=255)
    biography = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    start_date = models.DateTimeField(auto_now_add=True)
    advisors = models.ManyToManyField(Advisor, related_name="projects")
    researchers = models.ManyToManyField(Researcher, related_name="projects")
    sponsors = models.ManyToManyField(Sponsor, related_name="projects")
