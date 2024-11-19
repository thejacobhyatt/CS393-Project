from django.contrib import admin

# Register your models here.
from .models import Status, Department, Advisor, Researcher, Sponsor, ResearchProject

admin.site.register(Status)
admin.site.register(Department)
admin.site.register(Advisor)
admin.site.register(Researcher)
admin.site.register(Sponsor)
admin.site.register(ResearchProject)
