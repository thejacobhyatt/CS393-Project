from django.shortcuts import render
from django.http import HttpResponse
from .models import Researcher
from faker import Faker

def index(request):
    return HttpResponse("CS393 rocks! Use /add_fake_data to generate researchers or /show_fake_data to view them.")

def add_fake_data(request):
    fake = Faker()
    for _ in range(10):  # Generating 10 fake researchers
        Researcher.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
        )
    return HttpResponse("10 fake researchers have been added.")

def show_fake_data(request):
    researchers = Researcher.objects.all()
    template_name = "fake_data.html"
    context = {"researchers": researchers}
    return render(request, template_name, context)
