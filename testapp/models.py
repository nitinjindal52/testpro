from django.db import models

class Designations(models.Model):
    designation = models.CharField(max_length=200,unique=True)
    def __unicode__(self):
        return self.designation
    
class Department(models.Model):
    department = models.CharField(max_length=100,unique=True)
    def __unicode__(self):
        return self.department

class unit(models.Model):
    unit = models.CharField(max_length=100,unique=True)
    def __unicode__(self):
        return self.unit

class location(models.Model):
    location = models.CharField(max_length=100,unique=True)
    def __unicode__(self):
        return self.location

class level(models.Model):
    level = models.CharField(max_length=100,unique=True)
    def __unicode__(self):
        return self.level


class employee(models.Model):
    unit = models.ForeignKey(unit)
    old_employee_id = models.CharField(max_length=50, blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dateofbirth = models.DateField()
    dateofjoining = models.DateField()
    level = models.ForeignKey(level)
    designation = models.ForeignKey(Designations)
    department = models.ForeignKey(Department)
    email = models.EmailField(unique=True)
    location = models.ForeignKey(location)
    phone = models.BigIntegerField(unique=True, null=True, blank=True)
    skills = models.TextField(max_length=100, blank=True)
    reporting_person = models.IntegerField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return self.firstname   
    

    
class ProjectType(models.Model):
    type = models.CharField(max_length=100)
    description = models.TextField()
    def __unicode__(self):
        return self.type 
    
class Client(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    comments = models.TextField(blank=True)
    def __unicode__(self):
        return self.name
    
Status_Choices=(
                ('1','active'),
                ('2','inactive'))
   
class Project(models.Model):
    name = models.CharField(max_length=100,unique=True)
    type = models.ForeignKey(ProjectType)
    client = models.ForeignKey(Client)
    startdate = models.DateField()
    status=models.CharField(max_length=30,choices=Status_Choices)
    created_on=models.DateTimeField(auto_now_add=True)
    created_by=models.IntegerField()
    def __unicode__(self):
        return self.name
            
class Module(models.Model):
    module = models.CharField(max_length=100)
    def __unicode__(self):
        return self.module

class emp_project(models.Model):
    project = models.ForeignKey(Project)
    employee = models.ForeignKey(employee)
    approver = models.BooleanField(default=False)    
    def __unicode__(self):
        return self.project.name
    class Meta:
        unique_together = ('employee','project')
    
    def is_approver(self,empid):
        try:
            if self.objects.filter(employee=empid, approver=True):
                return True
            else:
                return False
        except Exception,error:
            return error
    
    
class Timesheet(models.Model):
    firstname = models.ForeignKey(employee)
    project = models.ForeignKey(Project)
    module = models.ForeignKey(Module)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4,decimal_places=2)
    comments = models.TextField(null=True, blank=True)
    edit = models.BooleanField()
    approved = models.BooleanField(default=False)
    approved_by = models.IntegerField(null=True, blank=True)
    approved_on = models.DateTimeField(null=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    
class Leave_type(models.Model):
    type = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.type

leave_Choices=(
                ('1','Morning'),
                ('2','Evening'),
                ('3','Full Day'))

class Leave_application(models.Model):
    employee = models.ForeignKey(employee)
    date_of_application = models.DateField()
    leave_start_date = models.DateField()
    leave_end_date = models.DateField() 
    leave_type = models.ForeignKey(Leave_type)
    remarks = models.TextField()
    Choices = models.CharField(max_length=10 ,choices=leave_Choices,default='3')
    approved = models.IntegerField(blank=True,null=True,default='0')
    approved_by = models.IntegerField(blank=True,null=True)
    approver_remarks = models.TextField(blank=True,null=True)
    token = models.CharField(max_length=50)
    status = models.CharField(max_length=5,choices=Status_Choices,default='1')
    def __unicode__(self):
        return self.employee.firstname
    
class Attendence(models.Model):
    employee = models.ForeignKey(employee)
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()
    duration = models.CharField(max_length=100)
    def __unicode__(self):
        return self.employee.firstname
    
class Optional_holidays(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    

    
#class designation(models.Model):
#    designation = models.CharField(max_length=100)
#    def __unicode__(self):
#        return self.designation
#    
#class role(models.Model):
#    employee = models.ForeignKey(employee, unique=True)
#    designation = models.ForeignKey(designation)
#    approver = models.BooleanField()
#    

    
   
      
            
        
    
    
        

