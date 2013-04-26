from models import *
from django.forms import ModelForm
from django import forms


class AttendenceForm(ModelForm):
    dd = forms.FileField()
    class Meta:
        model = Attendence
      

class EmployeeForm(ModelForm):
    dateofbirth = forms.DateField(widget=forms.TextInput( attrs={'class':'datepicker','readonly':'True'} ))
    dateofjoining = forms.DateField(widget=forms.TextInput( attrs={'class':'datepicker','readonly':'True'} ))
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'emp-input','onkeypress':'lettersOnly(event)'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'emp-input','onkeypress':'lettersOnly(event)'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'emp-input','onblur':'validateEmail(this);'}))
    
    
    class Meta:
        model = employee 
        
class ProjectTypeForm(ModelForm):
    
    class Meta:
        model = ProjectType
        
class ClientForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'emp-input'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class':'emp-input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'emp-input'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'class':'emp-textarea'}))
    
    class Meta:
        model = Client
        
class Emp_ProjectForm(ModelForm):
    class Meta:
        model = emp_project
    
class ProjectForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'emp-input'}))
    startdate = forms.DateField(widget=forms.TextInput( attrs={'class':'datepicker','readonly':'True'} ))
    class Meta:
        model = Project

class TimesheetForm(ModelForm):
    class Meta:
        model = Timesheet

class Leave_applicationForm(ModelForm):
    date_of_application = forms.CharField(widget=forms.TextInput(attrs={'class':'emp-input','readonly':'True'}))
    leave_start_date = forms.DateField(widget=forms.TextInput( attrs={'class':'emp-input','readonly':'True'} ))
    leave_end_date = forms.DateField(widget=forms.TextInput( attrs={'class':'emp-input','readonly':'True'} ))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'class':'emp-textarea','readonly':'True'}))
    class Meta:
        model = Leave_application

class TimesheettForm(ModelForm):
    
    class Meta:
        model = Timesheet()
class pmform(forms.Form):
    project = forms.CharField(max_length=150)
    employee = forms.CharField(max_length=150)
    
class EditForm(ModelForm):
    class Meta:
        model = Timesheet
        fields = ('project','module','date','hours','comments')