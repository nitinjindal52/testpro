# Create your views here.
from django.contrib import admin
from models import *
from django.forms import ModelForm
from django.contrib.auth.models import *
from django.core.mail import send_mail

class Employeeadmin(admin.ModelAdmin):
    pass

#admin.site.register(auth_user_groups)
admin.site.register((employee),Employeeadmin)
admin.site.register(ProjectType)
admin.site.register(Module)
admin.site.register(Project)
admin.site.register(Client)
admin.site.register(emp_project)
admin.site.register(Designations)
admin.site.register(Department)
admin.site.register(unit)
admin.site.register(location)
admin.site.register(level)
admin.site.register(Timesheet)
admin.site.register(Leave_type)
admin.site.register(Leave_application)