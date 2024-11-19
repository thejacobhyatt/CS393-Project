from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projects", views.project, name="project"),
    path("reseacher", views.researcher, name="researcher"),
    path("login", views.login, name="login")
]