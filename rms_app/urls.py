from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projects", views.project, name="project"),
    path("reseacher", views.researcher, name="researcher"),
    path("login", views.login_view, name="login"),
    path('add_project', views.add_project, name='add_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    path('your_project/', views.your_project, name='your_project'),
]