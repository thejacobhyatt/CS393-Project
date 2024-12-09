from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Researcher, Status, Department, Sponsor, Advisor, ResearchProject
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import logout
from django.shortcuts import redirect

def index(request):
    # Check if user belongs to Researcher or Advisors group
    is_researcher = request.user.groups.filter(name="Researcher").exists()
    is_advisor = request.user.groups.filter(name="Advisors").exists()

    # Pass these values to the template
    context = {
        'is_researcher': is_researcher,
        'is_advisor': is_advisor,
    }

    return render(request, 'rms_app/main.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, 'Login successful!')
            return redirect('index')  # Redirect to homepage or desired page after login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'rms_app/login.html')


def logout_view(request):
    logout(request)
    # messages.info(request, 'You have logged out successfully.')
    return redirect('index')

# In your view
from django.contrib.auth.models import Group

from django.contrib.auth.models import Group

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def your_view(request):
    # Checking if the user is in the "Researcher" or "Advisors" group
    is_researcher = request.user.groups.filter(name="Researcher").exists()
    is_advisor = request.user.groups.filter(name="Advisors").exists()

    context = {
        'is_researcher': is_researcher,
        'is_advisor': is_advisor,
    }
    return render(request, 'rms_app/main.html', context)


def project(request):
    is_researcher = request.user.groups.filter(name="Researcher").exists()
    is_advisor = request.user.groups.filter(name="Advisors").exists()

    data = ResearchProject.objects.prefetch_related('advisors', 'researchers', 'sponsors')
    for proj in data:
        print(f"Project: {proj.title}, Advisors: {[adv.first_name for adv in proj.advisors.all()]}")
    context = {'projects': data,
               'is_researcher': is_researcher,
                'is_advisor': is_advisor,}
    return render(request, "rms_app/project_list.html", context)

@login_required
def researcher(request):
    is_researcher = request.user.groups.filter(name="Researcher").exists()
    is_advisor = request.user.groups.filter(name="Advisors").exists()
    data = Researcher.objects.all()
    context = {'researchers': data,
               'is_researcher': is_researcher,
                'is_advisor': is_advisor,}
    return render(request, "rms_app/researcher_list.html", context)

@login_required
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(ResearchProject, pk=project_id)
        project.delete()
        return redirect('add_project')  # Redirect to the project list page after deletion

@login_required
def delete_project(request, project_id):
    # Check if the user is part of the "Advisors" group
    if not request.user.groups.filter(name="Advisors").exists():
        return redirect('project')  # Redirect to the projects page if not an advisor
    
    if request.method == 'POST':
        # Get the project to delete
        project = get_object_or_404(ResearchProject, pk=project_id)
        project.delete()
        return redirect('project')  # Redirect to the projects page after deletion

@login_required
def your_project(request):
    # Check if the user is in the Researcher or Advisor group
    is_researcher = request.user.groups.filter(name="Researcher").exists()
    is_advisor = request.user.groups.filter(name="Advisors").exists()

    # Get the current user
    user = request.user
    print(f"User: {user}")

    # Handle the case where the user might not be a researcher
    try:
        # Get the corresponding Researcher instance for the current user
        researcher = Researcher.objects.get(user=user)
        print(f"Researcher found: {researcher}")
    except Researcher.DoesNotExist:
        researcher = None  # Or you can return an error page or redirect
        print("Researcher does not exist for this user")

    # Filter projects associated with the current user (Researcher)
    if researcher:
        user_projects = ResearchProject.objects.filter(researchers=researcher)
        print(f"User's Projects: {user_projects}")
    else:
        user_projects = []  # No projects if the user is not a researcher
        print("No projects for non-researcher")

    # Pass the filtered projects to the context
    context = {
        'user_projects': user_projects,
        'is_researcher': is_researcher,
        'is_advisor': is_advisor,
    }
    
    # Return the template with the context
    return render(request, 'rms_app/your_project.html', context)



@login_required
def add_project(request):
    is_researcher = request.user.groups.filter(name="Researcher").exists()
    is_advisor = request.user.groups.filter(name="Advisors").exists()
    status = Status.objects.all()
    data = ResearchProject.objects.prefetch_related('advisors', 'researchers', 'sponsors')
    context = {'projects': data, 'statuses': status, 'is_researcher': is_researcher,
                'is_advisor': is_advisor,}

    if request.method == 'POST':
        title = request.POST.get('title')
        biography = request.POST.get('biography')
        status_name = request.POST.get('status')
        department_head = request.POST.get('department')
        start_date = request.POST.get('start_date')
        advisors_names = request.POST.get('advisors').split(',')
        researchers_names = request.POST.get('researchers').split(',')
        sponsors_names = request.POST.get('sponsors').split(',')

        try:
            # Get or create related objects
            status, _ = Status.objects.get_or_create(status_name=status_name)
            department, _ = Department.objects.get_or_create(department_head=department_head)
            
            # Create the research project
            project = ResearchProject.objects.create(
                title=title,
                biography=biography,
                status=status,
                department=department,
                start_date=start_date
            )
            
            # Add many-to-many relationships
            for advisor_name in advisors_names:
                first_name, last_name = advisor_name.strip().split(' ')
                advisor = Advisor.objects.get(first_name=first_name, last_name=last_name)
                project.advisors.add(advisor)

            for researcher_name in researchers_names:
                first_name, last_name = researcher_name.strip().split(' ')
                researcher = Researcher.objects.get(first_name=first_name, last_name=last_name)
                project.researchers.add(researcher)

            for sponsor_name in sponsors_names:
                sponsor = Sponsor.objects.get(name=sponsor_name.strip())
                project.sponsors.add(sponsor)
            
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect('project_list')  # Redirect to the project list page or any desired page
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    return render(request, 'rms_app/add_project.html', context)
