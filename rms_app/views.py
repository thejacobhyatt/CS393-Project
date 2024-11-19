from django.shortcuts import render
from .models import ResearchProject
from django.http import HttpResponse
from .models import Researcher
from faker import Faker

def index(request):
    return render(request, "rms_app/main.html")

def login(request):
    return render(request, "rms_app/login.html")

def project(request):
    data = ResearchProject.objects.all()
    context = {'projects': data}
    return render(request, "rms_app/project_list.html", context)

def researcher(request):
    data = Researcher.objects.all()
    context = {'researchers': data}
    return render(request, "rms_app/researcher_list.html", context)