#!python

from datetime import date, datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.aggregates import Sum
from piston.handler import BaseHandler
from testapp.models import Timesheet, employee, Project, Module, emp_project, \
    Leave_application, Leave_type
import hashlib

class UserHandler(BaseHandler):
    allowed_methods = ('GET')
    model = User
    def read(self,request):
        data = request.GET
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            employee_detail = employee.objects.get(email=username)
            projects_r = emp_project.objects.filter(employee = employee_detail)
            x = []
            for project in projects_r:
                project_sel = Project.objects.get(id=project.project_id)
                
                x.append({"project":project_sel.name})
                print x
                
            leave_type = Leave_type.objects.all()
            modules = Module.objects.all()
            data = {'employee':employee_detail,'projects':x,'modules':modules,'leave_type':leave_type}
            return data
        else:
            return "invalid "
        
class TimesheetHandler(BaseHandler):
    allowed_methods = ('GET','POST')
    model = Timesheet
    def read(self,request):
        username = request.user
        projects = emp_project.objects.filter(employee__email=username).values('project__name','project__id')
        employee_detail = employee.objects.get(email=username)
        module = Module.objects.all()
        data = {'projects':projects,'module':module,'employee':employee_detail}
        return data
        
    def create(self,request):
        if request.method == 'POST':
            data = request.POST
            usernamee = data['email']
            username = employee.objects.get(email=usernamee)
            projectt = data['project']
            project = Project.objects.get(name=projectt)
            modulee = data['module']
            module = Module.objects.get(module=modulee)
            date = data['date']
            hours = data['hours']
            comments = data['comments']
            status = data['status']
            try:
                
                Timesheet.objects.get(firstname=username,project=project,module=module,date=date)
                return {'status':"0"}
            except:
                #Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
                hours_sum = Timesheet.objects.filter(firstname=username.id,date=date).aggregate(Sum('hours'))
                d = float(hours)
                if hours_sum['hours__sum'] is None and d<15:
                    if status=="1":
                        Timesheet.objects.create(firstname=username,project=project,module=module,date=date,hours=hours,comments=comments)
                        return {'status':"1"}
                    else:
                        if status=="2":
                            Timesheet.objects.create(edit=1,firstname=username,project=project,module=module,date=date,hours=hours,comments=comments)
                            return {'status':"1"}
                else:
                    if d>15:
                        return {'status':"3"}
                    else:
                        if (float(hours_sum['hours__sum'])+d>15):
                            return {'status':"3"}
                        else:
                            if status=="1":
                                Timesheet.objects.create(firstname=username,project=project,module=module,date=date,hours=hours,comments=comments)
                                return {'status':"1"}
                            else:
                                if status=="2":
                                    Timesheet.objects.create(edit=1,firstname=username,project=project,module=module,date=date,hours=hours,comments=comments)
                                    return {'status':"1"}
                            
                    
                    
                
                
                        
class LeaveHandler(BaseHandler):
    allowed_methods = ('POST')
    model = Leave_application
    def create(self,request):
        data = request.POST
        usernamee = data['email']
        username = employee.objects.get(email=usernamee)
        date_of_application = date.today()
        leave_start_date = data['start_date']
        leave_end_date = data['end_date']
        leave_typee = data['leave_type']
        leave_type = Leave_type.objects.get(type=leave_typee)
        Choices = data['choices']
        remarks = data['remarks']
        token = hashlib.md5(str(datetime.now().isoformat())).hexdigest()
        try:
            Leave_application.objects.get(Choices=Choices,leave_type=leave_type,employee=username,date_of_application=date_of_application,leave_start_date=leave_start_date,leave_end_date=leave_end_date)
            return {'status':'0'}
        except:
            Leave_application.objects.create(token=token,remarks=remarks,Choices=Choices,leave_type=leave_type,employee=username,date_of_application=date_of_application,leave_start_date=leave_start_date,leave_end_date=leave_end_date)
            try:
                employee_reporter = username.reporting_person
                reporter = employee.objects.get(id=employee_reporter)
                employee_name = username.firstname+" "+username.lastname
                message = "hello "+employee_name+" has applied for a leave from date "+leave_start_date+" to "+leave_end_date+" "+Choices+" due to "+leave_typee+" .Remarks ( "+remarks+" ).To approve the leave click on http://115.248.233.133:8989/progazer/leave_approver/"+token+"/"
                subject = "Leave Application of "+employee_name
                send_mail(subject,message,"ProGazer@ProGazer.com",[reporter.email])
                return {'status':'1'}
            except:
                return {'status':'1'}
                
            
                