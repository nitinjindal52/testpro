from datetime import datetime, date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, \
    SetPasswordForm, UserCreationForm
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response, \
    get_object_or_404
from django.template import Context, loader, RequestContext
from testapp.forms import *
from testapp.models import *
import hashlib

def loginn(request):
    message="hello"
    try:
        user = request.user
        if user is not None:
            if user.is_active and not user.is_staff:
                return HttpResponseRedirect("/progazer/client_project/")
            else:
                pass
            if user.is_active and user.is_superuser:
                return HttpResponseRedirect("/progazer/admin_home/") 
            else:
                pass
            if user.is_active and (user.groups.filter(id=1).count()!=0):
                return HttpResponseRedirect("/progazer/admin_home_hr/") 
            else:
                pass
            if user.is_active and (user.groups.filter(id=2).count()!=0):
                return HttpResponseRedirect("/progazer/attendence/") 
            else:
                pass
            if user.is_active and user.is_staff:
                empid = employee.objects.get(email=user)
                print empid
                message ="Welcome Employee"
                try:
                    if emp_project.objects.filter(employee=empid,approver=1).count() != 0:
                        return HttpResponseRedirect("/progazer/viewtimesheet/")
                except:
                    return HttpResponseRedirect("/progazer/addtimesheet/")
    except:
        pass
    if request.POST:
        username =request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and not user.is_staff:
                login(request,user)
                return HttpResponseRedirect("/progazer/client_project/")
            else:
                pass
            if user.is_active and user.is_superuser:
                login(request,user)
                return HttpResponseRedirect("/progazer/admin_home/")
            else:
                pass
            if user.is_active and (user.groups.filter(id=1).count()!=0):
                login(request,user)
                return HttpResponseRedirect("/progazer/admin_home_hr/") 
            else:
                pass
            if user.is_active and (user.groups.filter(id=2).count()!=0):
                login(request,user)
                return HttpResponseRedirect("/progazer/attendence/") 
            else:
                pass
            if user.is_active and user.is_staff:
                login(request,user)
                empid = employee.objects.get(email=username)
                print empid
                message ="Welcome Employee"
                try:
                    if emp_project.objects.filter(employee=empid,approver=1).count() != 0:
                        return HttpResponseRedirect("/progazer/viewtimesheet/")
                    else:
                        return HttpResponseRedirect("/progazer/addtimesheet/")
                except:
                    return HttpResponseRedirect("/progazer/addtimesheet/")
        else:
            message = "Login Unsuccessful"
            return render_to_response('login.html',{message:'message','invalid': True },RequestContext(request))
    else:
        return render_to_response('login.html',{'message':message},RequestContext(request))

def admin_home_page(request):
    if request.user.is_active and request.user.is_superuser:
        email = request.user
        employee_name = employee.objects.get(email=email)
        user_name = employee_name.firstname
        return render_to_response('admin_home.html',{'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def admin_home_page_hr(request):
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        email = request.user
        employee_name = employee.objects.get(email=email)
        user_name = employee_name.firstname
        return render_to_response('admin_home_hr.html',{'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")



def logoutuser(request):
    logout(request)
    return HttpResponseRedirect("/progazer/login/")

def forgotpswrd(request):
    if request.POST:
        username = request.POST.get('email')
        try:
            email = username
            new_password = User.objects.make_random_password()
            u = User.objects.get(username__exact=username)
            u.set_password(new_password)
            u.save()
            message = "Your new password is "+new_password +" and login id is " +email
            send_mail("Password Recovery",message,"ProGazer@ProGazer.com",[email])
            return render_to_response('forgot_password.html',{'pop':'1'},RequestContext(request))
        except :
            return render_to_response('forgot_password.html',{'pop':'2'},RequestContext(request))
    else:    
        return render_to_response('forgot_password.html',{'pop':'0'},RequestContext(request))

def change_passwordd(request):
    user = request.user
    if user.is_active:
        user=request.user
        employee_name = employee.objects.get(email=user)
        user_name = employee_name.firstname
        try:
            if emp_project.objects.filter(employee=employee_name.id,approver=1).count() != 0:
                user_status = '2'
            else:
                user_status = '0'
        except:
            user_status = '0'
        if user.is_staff and user.is_superuser:
            user_status = '1'
        
        if request.user.is_active and (request.user.groups.filter(id=1).count()!=0) and (request.user.groups.filter(id=2).count()!=0):
            user_status = '3'
        if request.user.is_active and (request.user.groups.filter(id=1).count()==0) and (request.user.groups.filter(id=2).count()!=0):
            user_status = '4'
            
        if request.method=='POST':
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            if user.check_password(old_password) == True:
                u = User.objects.get(username__exact=user)
                u.set_password(new_password)
                u.save()
                return HttpResponseRedirect("/progazer/login")
            else:
                return render_to_response('change_password.html',{'user_name':user_name,'user_status':user_status,'popup':'1','username':user},RequestContext(request))
        return render_to_response('change_password.html',{'user_name':user_name,'user_status':user_status,'username':user},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login")


def employeee(request):
    user = request.user
    logger = employee.objects.get(email=user)
    user_name = logger.firstname
    user_id = logger.id
    if user.is_active and (user.groups.filter(id=1).count()!=0):
        employee_list = employee.objects.all()
        form=EmployeeForm()
        if request.method=='POST':
            form=EmployeeForm(request.POST)
            if form.is_valid():
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                dateofbirth = request.POST['dateofbirth']
                email = request.POST['email']
                print firstname, lastname, dateofbirth
                try:
                    employee.objects.get(firstname=firstname,lastname=lastname,dateofbirth=dateofbirth)
                    return render_to_response('employee.html',{'user_name':user_name,'user_id':user_id,'popup':'2','form':form},RequestContext(request))
                except:
                    username = email
                    password = User.objects.make_random_password()
                    user = User.objects.create_user(username, email,password)
                    user.is_staff = True
                    user.is_active = True
                    user.save()
                    message = "your password is "+password +" and login id is " +email
                    send_mail("login details",message,"ProGazer@ProGazer.com",[email])
                    form.save()
                    form=EmployeeForm()
                    return render_to_response('employee.html',{'user_name':user_name,'user_id':user_id,'popup':'1','employee_list':employee_list,'form':form},RequestContext(request))
            else:
                form=EmployeeForm(request.POST) 
                return render_to_response('employee.html',{'user_name':user_name,'user_id':user_id,'popup':'3','employee_list':employee_list,'form':form},RequestContext(request))
        else:
            return render_to_response('employee.html',{'user_name':user_name,'user_id':user_id,'employee_list':employee_list,'form':form},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def optional_holiday(request):
    user = request.user
    employee_name = employee.objects.get(email=user)
    user_name = employee_name.firstname
    if user.is_active and (user.groups.filter(id=1).count()!=0):
        optional = Optional_holidays.objects.all()
        if request.method=='POST':
            if 'add' in request.POST:
                date = request.POST['new_date']
                name = request.POST['leave_name']
                if date=="" or name=="":
                    return render_to_response('view_optional_holiday.html',{'message':"Date or holiday can't be null.",'optional':optional,'user_name':user_name},RequestContext(request))
                else:    
                    try:
                        Optional_holidays.objects.get(date=date)
                        return render_to_response('view_optional_holiday.html',{'message':"Duplicate entry.",'optional':optional,'user_name':user_name},RequestContext(request))
                    except:
                        Optional_holidays.objects.create(date=date,name=name)
                        optional = Optional_holidays.objects.all()
                        return render_to_response('view_optional_holiday.html',{'optional':optional,'user_name':user_name},RequestContext(request))
            if 'remove' in request.POST:
                id_l = request.POST['id']
                Optional_holidays.objects.filter(id=id_l).delete()
                optional = Optional_holidays.objects.all()
                return render_to_response('view_optional_holiday.html',{'optional':optional,'user_name':user_name},RequestContext(request))
        else:
            return render_to_response('view_optional_holiday.html',{'optional':optional,'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def leave_register_hr(request):
    user = request.user
    employee_name = employee.objects.get(email=user)
    user_name = employee_name.firstname
    if user.is_active and (user.groups.filter(id=1).count()!=0):
        leaves = Leave_application.objects.all().order_by("-date_of_application","-id")
        return render_to_response('leave_register_hr.html',{'user_name':user_name,'leaves':leaves},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
        
    
def view_leave_hr_id(request,token):
    user = request.user
    if user.is_active and (user.groups.filter(id=1).count()!=0):
        employee_user = employee.objects.get(email=user)
        application = Leave_application.objects.get(token=token)
        application_id = str(application.id)
        form = Leave_applicationForm( instance=application )
        employee_id = application.employee.id
        employee_requester = employee.objects.get(id=employee_id)
        employee_name = employee_requester.firstname+" "+employee_requester.lastname
        application_date = application.date_of_application
        start_date =application.leave_start_date
        end_date = application.leave_end_date
        ch = application.Choices
        remarks = application.remarks
        approver_remarks = application.approver_remarks
        if (ch=='1'):
            choices='Morning'
        else:
            if (ch=='2'):
                choices='Evening'
            else:
                choices='Full Day'
        leave_type = application.leave_type
        if request.method=='POST':
            if 'approve' in request.POST:
                hr_message = request.POST['hr_remarks']
                Leave_application.objects.filter(token=token).update(approved=1,approved_by=employee_user.id)
                message = "Hello, Your leave application with ID"+application_id+" is approved. HR Remarks ("+hr_message+" )."
                subject = "Leave Application ID: "+application_id+" Approved"
                send_mail(subject,message,"progazer@progazer.com",[employee_requester.email])
                try:
                    employee_reporter_id = employee_requester.reporting_person
                    reporter = employee.objects.get(id=employee_reporter_id)
                    reporter_email = reporter.email
                    message = "Hello, Leave application of "+employee_requester.firstname+" is approved. HR Remarks ("+hr_message+" )."
                    subject = "Leave Application ID: "+application_id+" of "+employee_requester.firstname+" is approved by HR "+employee_user.firstname+" ."
                    send_mail(subject,message,"progazer@progazer.com",[reporter_email])
                    return HttpResponseRedirect("/progazer/leave_register_hr/")
                except:
                    return HttpResponseRedirect("/progazer/leave_register_hr/")
            if 'reject' in request.POST:
                hr_message = request.POST['hr_remarks']
                Leave_application.objects.filter(token=token).update(approved=2,approved_by=employee_user.id)
                message = "Hello, Your leave application with ID"+application_id+" is Rejected. HR Remarks ("+hr_message+" )."
                subject = "Leave Application ID: "+application_id+" Rejected"
                send_mail(subject,message,"progazer@progazer.com",[employee_requester.email])
                try:
                    employee_reporter_id = employee_requester.reporting_person
                    reporter = employee.objects.get(id=employee_reporter_id)
                    reporter_email = reporter.email
                    message = "Hello, Leave application of "+employee_requester.firstname+" is approved. HR Remarks ("+hr_message+" )."
                    subject = "Leave Application ID: "+application_id+" of "+employee_requester.firstname+" is rejected by HR "+employee_user.firstname+" ."
                    send_mail(subject,message,"progazer@progazer.com",[reporter_email])
                    return HttpResponseRedirect("/progazer/leave_register_hr/")
                except:
                    return HttpResponseRedirect("/progazer/leave_register_hr/")
        else:
            
            return render_to_response('leave_approver_hr.html',{'application':application,'approver_remarks':approver_remarks,'leave_type':leave_type,'choices':choices,'remarks':remarks,'start_date':start_date,'end_date':end_date,'employee_name':employee_name,'application_date':application_date,'form':form},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
    
def employee_view(request):
    user = request.user
    if user.is_active and (user.groups.filter(id=1).count()!=0):
        employee_list = employee.objects.all()
        if request.method == 'POST':
            if 'export' in request.POST:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Progazer_Employee_data.csv"'

                writer = csv.writer(response)
                writer.writerow(['ID','Unit','Name','Old id','Date of birth','Date of joining','Level','Designation','Department','Email','Location','Phone'])
                rr = employee.objects.all().order_by('firstname')
                for r in rr:
                    name=r.firstname+" "+r.lastname
                    writer.writerow([r.id,r.unit,name,r.old_employee_id,r.dateofbirth,r.dateofjoining,r.level,r.designation,r.department,r.email,r.location,r.phone])
                return response
            name=request.POST['employee']
            x = name.split()
            if len(x)==1:
                employee_list = employee.objects.filter(firstname=name).all()
                print len(employee_list)
                if len(employee_list)!=0:            
                    return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
                else:
                    print "in sort else"
                    employee_list = employee.objects.filter(lastname=name).all()
                    return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
            if len(x)==2:
                print "length 2"
                firstname = x[0]
                lastname = x[1]
                firstname_middle = x[0]+" "+x[1]
                print firstname_middle
                employee_list = employee.objects.filter(firstname=firstname_middle).all() | employee.objects.filter(firstname=firstname).all()
                if len(employee_list)!=0:            
                    return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))    
                else:
                    employee_list = employee.objects.filter(lastname=lastname).all()
                    if len(employee_list)!=0:
                        return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
                    else:
                        employee_list=employee.objects.filter(firstname=firstname).all()
                        return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
            if len(x)==3:
                firstname = x[0]+" "+x[1]
                lastname = x[2]
                employee_list=employee.objects.filter(firstname=firstname,lastname=lastname).all()
                return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
            else:
                return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'ID(ascending)'},RequestContext(request))
        else:
            return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'ID(ascending)'},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
    
def employee_view_sorted(request,element):
    user = request.user
    if user.is_active and (user.groups.filter(id=1).count()!=0):
        if request.method == 'POST':
            if 'export' in request.POST:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Progazer_Employee_data.csv"'

                writer = csv.writer(response)
                writer.writerow(['ID','Unit','Name','Old id','Date of birth','Date of joining','Level','Designation','Department','Email','Location','Phone'])
                rr = employee.objects.all().order_by('firstname')
                for r in rr:
                    name=r.firstname+" "+r.lastname
                    writer.writerow([r.id,r.unit,name,r.old_employee_id,r.dateofbirth,r.dateofjoining,r.level,r.designation,r.department,r.email,r.location,r.phone])
                return response
            name=request.POST['employee']
            x = name.split()
            if len(x)==1:
                employee_list = employee.objects.filter(firstname=name).all()
                print len(employee_list)
                if len(employee_list)!=0:            
                    return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
                else:
                    print "in sort else"
                    employee_list = employee.objects.filter(lastname=name).all()
                    return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
            if len(x)==2:
                print "length 2"
                firstname = x[0]
                lastname = x[1]
                firstname_middle = x[0]+" "+x[1]
                print firstname_middle
                employee_list = employee.objects.filter(firstname=firstname_middle).all() | employee.objects.filter(firstname=firstname).all()
                if len(employee_list)!=0:            
                    return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))    
                else:
                    employee_list = employee.objects.filter(lastname=lastname).all()
                    if len(employee_list)!=0:
                        return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
                    else:
                        employee_list=employee.objects.filter(firstname=firstname).all()
                        return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
            if len(x)==3:
                firstname = x[0]+" "+x[1]
                lastname = x[2]
                employee_list=employee.objects.filter(firstname=firstname,lastname=lastname).all()
                return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'------'},RequestContext(request))
                           
            
        else:
            pass
        if element == '4' :
            print "in if"
            name = "-firstname"
            employee_list = employee.objects.all().order_by(name)
            return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'Name(descending)'},RequestContext(request))
        if element == '3' :
            print "in if"
            name = "firstname"
            employee_list = employee.objects.all().order_by(name)
            return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'Name(ascending)'},RequestContext(request))
        if element == '2' :
            print "in if"
            name = "-id"
            employee_list = employee.objects.all().order_by(name)
            return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'ID(descending)'},RequestContext(request))
        
        else:
            print "in else"
            employee_list = employee.objects.all()
        
            return render_to_response('view_employee.html',{'employee_list':employee_list,'sort_value':'ID(ascending)'},RequestContext(request))
        
    else:
        return HttpResponseRedirect("/progazer/login/")
            
def employee_view_id(request,employee_id):
    user = request.user
    if user.is_active and (user.groups.filter(id=1).count()!=0):
        employee_list = employee.objects.all().order_by('firstname')
        print employee_id
        selected_employee = employee.objects.get( id=employee_id )
        try:
            person = employee.objects.get(id=selected_employee.reporting_person)
            reporting_person_value = person.id        
            reporting_person = person.firstname+" "+person.lastname
        except:
            reporting_person = "Not Alloted"
            reporting_person_value = '0'
        
        form = EmployeeForm( instance=selected_employee )
        if request.method=='POST':
            form = EmployeeForm(request.POST, instance=selected_employee)
            try:
                try:
                    form.save()
                    return HttpResponseRedirect("/progazer/view_employee/")
                except Exception, e:
                    print e
                    return render_to_response('errors.html',{'form':form},RequestContext(request))
                else:
                    return HttpResponse("not valid")
            except Exception,e:
                print e
        else:        
            return render_to_response('view_employee_id.html',{'reporting_person_value':reporting_person_value,'reporting_person':reporting_person,'employee_list':employee_list,'form':form,'employee':selected_employee},RequestContext(request))    
    else:
        return HttpResponseRedirect("/progazer/login/")
    
   
def addclientt(request):
    user = request.user
    logger = employee.objects.get(email=user)
    user_name=logger.firstname
    if user.is_active and user.is_superuser:
        message = ""
        form = ClientForm()
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                username = email
                password = User.objects.make_random_password()
                try:
                    user = User.objects.create_user(username, email,password)
                    user.is_active = True
                    user.save()
                    message = "your password is "+password +" and login id is " +email
                    send_mail("login details",message,"ProGazer@ProGazer.com",[email])
                    form.save()
                    return HttpResponseRedirect("/progazer/login/")
                except:
                    message = "User with this email already exist."
                    return render_to_response('client.html',{'user_name':user_name,'message':message,'form':form},RequestContext(request))
            else:
                return render_to_response('client.html',{'user_name':user_name,'message':message,'form':form},RequestContext(request))
        else:
            return render_to_response('client.html',{'user_name':user_name,'message':message,'form':form},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def view_clientt(request):
    user = request.user
    zz = employee.objects.get(email=user)
    user_name = zz.firstname
    if user.is_active and user.is_superuser:
        client_list = Client.objects.all()
        return render_to_response('view_client.html',{'user_name':user_name,'client':client_list},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def client_view_id(request,client_id):
    user = request.user
    logger = employee.objects.get(email=user)
    user_name=logger.firstname
    if user.is_active and user.is_superuser:
        client = Client.objects.get(id=client_id)
        if request.method=='POST':
            form = ClientForm(request.POST)
            company = request.POST['company']
            comments = request.POST['comments']
            if company != "" and comments != "":
                Client.objects.filter(id=client_id).update(company=company,comments=comments)
                return HttpResponseRedirect("/progazer/view_client/")
            else:
                print form.errors
                return render_to_response('view_client_id.html',{'user_name':user_name,'form':form,'client':client},RequestContext(request))
        else:
            return render_to_response('view_client_id.html',{'user_name':user_name,'client':client},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

    
def addprojectt(request):
    user = request.user
    logger = employee.objects.get(email=user)
    user_name=logger.firstname
    user_id = logger.id
    if user.is_active and user.is_superuser:
        message = "error in saving project"
        form = ProjectForm()
        if request.method == 'POST':
            userlogged = employee.objects.get(email=user)
            user_id = userlogged.id
            print "done"
            form = ProjectForm(request.POST)
            if form.is_valid():
                print "form is valid"
                form.save()
                return HttpResponseRedirect("/progazer/admin_home/")
            else:
                print "form is invalid"
                return render_to_response('project.html',{'user_name':user_name,'user_id':user_id,'message':message,'form':form},RequestContext(request))
        else:
            return render_to_response('project.html',{'user_name':user_name,'user_id':user_id,'form':form},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def view_projectt(request):
    user = request.user
    zz = employee.objects.get(email=user)
    user_name = zz.firstname
    if user.is_active and user.is_superuser:
        project_list = Project.objects.all()
        return render_to_response('view_project.html',{'user_name':user_name,'project':project_list},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def project_view_id(request,project_id):
    user = request.user
    zz = employee.objects.get(email=user)
    user_name = zz.firstname
    if user.is_active and user.is_superuser:
        project = Project.objects.get(id=project_id)
        form = ProjectForm(instance=project)
        if request.method=='POST':
            startdate = request.POST['startdate']
            status = request.POST['status']
            Project.objects.filter(id=project_id).update(startdate=startdate,status=status)
            return HttpResponseRedirect("/progazer/view_project/")
        else:
            return render_to_response('view_project_id.html',{'user_name':user_name,'form':form,'project':project},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
    

#def editt(request,time_id,year,month,day):
#    if request.user.is_authenticated():
#        obj = Timesheet.objects.get(id=time_id,edit=0)
#        form = TimesheetForm()
#        date = year+"-"+month+"-"+day
#        message = "record not updated"
#        message1 = "record updated" 
#        if request.method =='POST':
#            hours = request.POST['hours']
#            comments = request.POST['comments']
#            print hours, comments
#            try:
#                Timesheet.objects.filter(id=time_id).update(hours=hours,comments=comments)
#    #            return HttpResponse('/addtimesheeett/'.render(Context({'selected_date':date}))
#                return render_to_response('timesheetupdated.html',{'selected_date':date,'message':message1,'obj':obj},context_instance=RequestContext(request))
#            except:
#                return render_to_response('timesheetupdated.html',{'selected_date':date,'message':message,'obj':obj},context_instance=RequestContext(request))
#        else:
#            return render_to_response('edit.html',{'form':form,'obj':obj},context_instance=RequestContext(request))
#    else:
#        return HttpResponse("you are not employee")
    
    
def addtimesheett_withoutdate(request):
    if request.user.is_authenticated()and request.user.is_staff:
        user=request.user
        employee_name = employee.objects.get(email=user)
        try:
            if emp_project.objects.filter(employee=employee_name.id,approver=1).count() != 0:
                user_status = '2'
            else:
                user_status = '0'
        except:
            user_status = '0'
        if user.is_staff and user.is_superuser:
            user_status = '1'
        modules = Module.objects.all()
        email = request.user
        employee_name = employee.objects.get(email=email)
        user_name = employee_name.firstname
        form = TimesheetForm() 
        employee_id = employee_name.id
        assigned_project = emp_project.objects.filter(employee=employee_id).all()
        return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'project':assigned_project,'form':form,'name':employee_name},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")



def addtimesheett(request,year,month,day):
    if request.user.is_authenticated() and request.user.is_staff:
        user=request.user
        employee_name = employee.objects.get(email=user)
        try:
            if emp_project.objects.filter(employee=employee_name.id,approver=1).count() != 0:
                user_status = '2'
            else:
                user_status = '0'
        except:
            user_status = '0'
        if user.is_staff and user.is_superuser:
            user_status = '1'
        print user_status
        modules = Module.objects.all()
        message1 = "Timesheet Already Exist"
        message2 = "Invalid Format"
        email = request.user
        user_name = employee_name.firstname
        form = TimesheetForm() 
        employee_id = employee_name.id
        assigned_project = emp_project.objects.filter(employee=employee_id).all()
        date = year+"-"+month+"-"+day
        sum_hours = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
#        date = datetime.date.today()
        timesheets_editable = Timesheet.objects.filter(firstname=employee_id,date=date,edit=0).all()
        timesheets_noneditable = Timesheet.objects.filter(firstname=employee_id,date=date,edit=1).all()
        if request.method=='POST':
            if 'edit' in request.POST:
                record_id = request.POST['record_id']
                obj = Timesheet.objects.get(id=record_id,edit=0)
                return render_to_response('edit_timesheet.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'obj':obj,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
            else:
                pass
            if 'update' in request.POST:
                record_update_id = request.POST['record_update_id']
                hours = request.POST['hours']
                comments = request.POST['comments']
                hours = request.POST['hours']
                g = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
                i = float(hours)
                if  (i > 15):
                    obj = Timesheet.objects.get(id=record_update_id,edit=0)
                    return render_to_response('edit_timesheet.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'obj':obj,'message':"Total hours can't be more than 15 hours.",'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                else:
                    obj = Timesheet.objects.get(id=record_update_id,edit=0)
                    jh = float(obj.hours)    
                    if (float(g['hours__sum'])-jh+i >15):
                        return render_to_response('edit_timesheet.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'obj':obj,'message':"Total hours can't be more than 15 hours.",'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                    else:
                        try:
                            Timesheet.objects.filter(id=record_update_id).update(hours=hours,comments=comments)
                            timesheets_editable = Timesheet.objects.filter(firstname=employee_id,date=date,edit=0).all()
                            timesheets_noneditable = Timesheet.objects.filter(firstname=employee_id,date=date,edit=1).all()
                            sum_hours = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))       
                            return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                        except Exception:
                            obj = Timesheet.objects.get(id=record_update_id,edit=0)
                            return render_to_response('edit_timesheet.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'obj':obj,'message':"Invalid Update",'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
            else:
                pass   
            if 'submit_record' in request.POST:
                record_id = request.POST['record_id']
                Timesheet.objects.filter(id=record_id).update(edit=1)
                timesheets_editable = Timesheet.objects.filter(firstname=employee_id,date=date,edit=0).all()
                timesheets_noneditable = Timesheet.objects.filter(firstname=employee_id,date=date,edit=1).all()
                sum_hours = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))       
                return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
            else:
                pass
            if 'save' in request.POST:
                form = TimesheetForm(request.POST)
                print form
                if form.is_valid():
                    firstname = request.POST['firstname']
                    project = request.POST['project']
                    module = request.POST['module']
                    date = request.POST['date']
                    hours = request.POST['hours']
                    try:
                        Timesheet.objects.get(firstname=firstname,project=project,module=module,date=date)
                        return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':message1,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                    except:
                        g = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
                        print g
                        i = float(hours)
                        print g['hours__sum']
                        if (g['hours__sum'] is None and i < 15 ):
                            form.save()
                            sum_hours = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
                            return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                        print hours
                        if  (i > 15):
                            print "here"
                            return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':"Total hours can't be more than 15 hours.",'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                        else:
                            
                            if (float(g['hours__sum'])+i >15):
                                return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':"Total hours can't be more than 15 hours.",'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                            else:
                                form.save()
                                sum_hours = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
                                return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                else:
                    return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':message2,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))      
            if 'submit' in request.POST:
                form = TimesheetForm(request.POST)
                if form.is_valid():
                    firstname = request.POST['firstname']
                    project = request.POST['project']
                    module = request.POST['module']
                    date = request.POST['date']
                    hours = request.POST['hours']
                    try:
                        Timesheet.objects.get(firstname=firstname,project=project,module=module,date=date)
                        return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':message1,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                    
                    except:
                        g = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
                        print g
                        i = float(hours)
                        print g['hours__sum']
                        if (g['hours__sum'] is None and i < 15 ):
                            form.save()
                            sum_hours = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))
                            return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                        print hours
                        if  (i > 15):
                            print "here"
                            return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':"Total hours can't be more than 15 hours.",'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                        else:
                            
                            if (float(g['hours__sum'])+i >15):
                                return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':"Total hours can't be more than 15 hours.",'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                            else:
                                form.save()
                                t = Timesheet.objects.get( firstname=firstname, project=project, module=module, date=date )
                                t.edit = True
                                t.save()
                                sum_hours = Timesheet.objects.filter(firstname=employee_id,date=date).aggregate(Sum('hours'))       
                                return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
                else:
                    return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'message':message2,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
        else:
            return render_to_response('timesheet1.html',{'user_status':user_status,'user_name':user_name,'modules':modules,'timespent':sum_hours,'project':assigned_project,'form':form,'name':employee_name,'selected_date':date,'record_date':timesheets_editable,'ts_date':timesheets_noneditable},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
        

def viewtimesheett_pre(request):
    username= request.user
    empid = employee.objects.get(email=username)
    user_name = empid.firstname
    assigned_project = emp_project.objects.filter(employee=empid,approver=1).all()
    if username.is_superuser:
        user_status ='1'
    else:
        user_status ='0'
    if request.method == 'POST':
        proj = request.POST['project']
        proj_name = Project.objects.get(id=proj)
        employees = emp_project.objects.filter(project=proj).all()
        return render_to_response('project_manager1.html',{'user_status':user_status,'user_name':user_name,'assigned_project':assigned_project,'empl':employees,'project':proj_name,'project_id':proj},RequestContext(request))
    else:
        return render_to_response('project_manager.html',{'user_status':user_status,'user_name':user_name,'assigned_project':assigned_project},RequestContext(request))

def viewtimesheett_pre_withproject(request,project_id):
    user = request.user
    username= request.user
    if username.is_superuser:
        user_status ='1'
    else:
        user_status ='0'
    empid = employee.objects.get(email=username)
    user_name = empid.firstname
    assigned_project = emp_project.objects.filter(employee=empid,approver=1).all()
    if project_id=='0':
        return render_to_response('project_manager1.html',{'user_status':user_status,'user_name':user_name,'user':user,'assigned_project':assigned_project,'project_id':project_id},RequestContext(request))
    else:
        project_name = Project.objects.get(id=project_id)
        employees = emp_project.objects.filter(project=project_id).all()
        return render_to_response('project_manager1.html',{'user_status':user_status,'user_name':user_name,'user':user,'assigned_project':assigned_project,'empl':employees,'project':project_name,'project_id':project_id},RequestContext(request))


def viewtimesheett(request,project_id,employee_id):
    if request.user.is_authenticated():
        email=request.user
        if email.is_superuser:
            user_status ='1'
        else:
            user_status ='0'
        zz = employee.objects.get(email=email)
        user_name = zz.firstname
        empid = zz.id
        emp_project.objects.get(employee=empid,approver=1,project=project_id)
        obj = Timesheet.objects.filter(edit=1,approved=0,project=project_id,firstname=employee_id).all()
        obja = Timesheet.objects.filter(edit=1,approved=1,project=project_id,firstname=employee_id).all()
        if request.method=='POST':
            if 'approve' in request.POST:
                record_id = request.POST['record_id']
                selected_record = Timesheet.objects.get(id=record_id) 
                return render_to_response('approval_timesheet.html',{'user_status':user_status,'user_name':user_name,'record':selected_record},RequestContext(request))
            if 'final_approve' in request.POST:
                record_id = request.POST['record_id']
                Timesheet.objects.filter(id=record_id).update(approved=1,approved_by=empid,approved_on=datetime.now())
                obj = Timesheet.objects.filter(edit=1,approved=0,project=project_id,firstname=employee_id).all()
                obja = Timesheet.objects.filter(edit=1,approved=1,project=project_id,firstname=employee_id).all()
                return render_to_response('view_timesheets.html',{'user_status':user_status,'user_name':user_name,'record':obj,'record_a':obja},RequestContext(request))
            if 'discard' in request.POST:
                record_id = request.POST['record_id']
                selected_record = Timesheet.objects.get(id=record_id)
                return render_to_response('discard_timesheet.html',{'user_status':user_status,'user_name':user_name,'record':selected_record},RequestContext(request))
            if 'final_discard' in request.POST:
                record_id = request.POST['record_id']
                x = Timesheet.objects.get(id=record_id)
                Timesheet.objects.filter(id=record_id).update(edit=0)
                messageq = request.POST['discard_reason']
                project = str(x.project.name)
                module = str(x.module.module)
                date = str(x.date)
                address = x.firstname.email
                message = "your submitted timesheet on project  "+project +" ,Activity "+module +" on date "+date +" is discarded due to "+messageq
                send_mail("timesheet discarded",message,"ProGazer@ProGazer.com",[address])
                obj = Timesheet.objects.filter(edit=1,approved=0,project=project_id,firstname=employee_id).all()
                obja = Timesheet.objects.filter(edit=1,approved=1,project=project_id,firstname=employee_id).all()
                return render_to_response('view_timesheets.html',{'user_status':user_status,'user_name':user_name,'record':obj,'record_a':obja},RequestContext(request))
        else:
            return render_to_response('view_timesheets.html',{'user_status':user_status,'user_name':user_name,'record':obj,'record_a':obja},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
    
def client_projectt(request):
    email = request.user
    client = Client.objects.get(email=email)
    print client.id   
    projects = Project.objects.filter(client=client.id).all()
    return render_to_response('client_project.html',{'client':client,'projects':projects},RequestContext(request))
    
def client_project_timesheett(request, project_id):
    timesheets = Timesheet.objects.filter(project=project_id,approved=1)
    return render_to_response('client_project_timesheet.html',{'timesheets':timesheets},RequestContext(request))

def assign_projectt(request):
    user = request.user
    if user.is_active and user.is_superuser:
        zz = employee.objects.get(email=user)
        user_name = zz.firstname
        projects = Project.objects.all()
        units = unit.objects.all()
        departments = Department.objects.all()
        return render_to_response('assign_project.html',{'user_name':user_name,'selected_project':"",'selected_department':"",'selected_unit':"",'unit':units,'department':departments,'project':projects},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
    
    
def assign_projectt_projectid(request,project_id,department_id,unit_id):
    user = request.user
    if user.is_active and user.is_superuser :
        zz = employee.objects.get(email=user)
        user_name = zz.firstname
        form = Emp_ProjectForm()
        projects = Project.objects.all()
        units = unit.objects.all()
        assigned_employee = emp_project.objects.filter(project=project_id)
        x = []
        for y in assigned_employee:
            x.append(y.employee.id)
        departments = Department.objects.all()
        selected_project = Project.objects.get(id = project_id)
        if unit_id == "0" and department_id != "0":
            selected_unit = ""
            selected_department = Department.objects.get(id = department_id)
            employee_list = employee.objects.filter(department=department_id)
        else:
            if unit_id != "0" and department_id == "0":
                selected_unit = unit.objects.get(id=unit_id)
                selected_department = ""
                employee_list = employee.objects.filter(unit=unit_id)
            else:
                if unit_id =="0" and department_id == "0":
                    selected_unit=""
                    selected_department = ""
                    employee_list = employee.objects.all()
                else:
                    selected_unit = unit.objects.get(id=unit_id)
                    selected_department = Department.objects.get(id = department_id)
                    employee_list = employee.objects.filter(department=department_id,unit=unit_id)
        if request.method=='POST':
            emp_id = request.POST['employee_name']
            selected_emp = employee.objects.get(id=emp_id)
            selected_project = Project.objects.get(id=project_id)
            try:
                xw = request.POST['checkbox'] =='on'
                emp_project.objects.create(employee=selected_emp,project=selected_project,approver=True)
                assigned_employee = emp_project.objects.filter(project=project_id)
                x = []
                for y in assigned_employee:
                    x.append(y.employee.id)
                return render_to_response('assign_project.html',{'user_name':user_name,'selected_unit':selected_unit,'unit':units,'x':x,'selected_project':selected_project,'selected_department':selected_department,'department':departments,'form':form,'project':projects,'employee_list':employee_list},RequestContext(request))
            except Exception:
                try:
                    emp_project.objects.create(employee=selected_emp,project=selected_project)
                    assigned_employee = emp_project.objects.filter(project=project_id)
                    x = []
                    for y in assigned_employee:
                        x.append(y.employee.id)
                    return render_to_response('assign_project.html',{'user_name':user_name,'selected_unit':selected_unit,'unit':units,'x':x,'selected_project':selected_project,'selected_department':selected_department,'department':departments,'form':form,'project':projects,'employee_list':employee_list},RequestContext(request))
                except Exception:
                    assigned_employee = emp_project.objects.filter(project=project_id)
                    x = []
                    for y in assigned_employee:
                        x.append(y.employee.id)
                    return render_to_response('assign_project.html',{'user_name':user_name,'selected_unit':selected_unit,'unit':units,'x':x,'popup':'1','selected_project':selected_project,'selected_department':selected_department,'department':departments,'form':form,'project':projects,'employee_list':employee_list},RequestContext(request))
        else:
            return render_to_response('assign_project.html',{'user_name':user_name,'selected_unit':selected_unit,'unit':units,'x':x,'selected_project':selected_project,'selected_department':selected_department,'department':departments,'form':form,'project':projects,'employee_list':employee_list},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
    
def re_assign_projectt(request):
    user = request.user
    zz = employee.objects.get(email=user)
    user_name = zz.firstname
    if user.is_active and user.is_superuser:
        project = Project.objects.all()
        return render_to_response('reassign_project_select.html',{'selected_project':"",'user_name':user_name,'project':project},RequestContext(request))    
    else:
        return HttpResponseRedirect("/progazer/login/")
    
def re_assign_project_with_id(request,project_id):
    user = request.user
    zz = employee.objects.get(email=user)
    user_name = zz.firstname
    if user.is_active and user.is_superuser:
        project = Project.objects.all()
        selected_project = Project.objects.get(id=project_id)
        employee_list = emp_project.objects.filter(project=selected_project)
        if request.method=='POST':
            record_id = request.POST['record_id']
            x = emp_project.objects.get(id=record_id)
            x.delete()
            employee_list = emp_project.objects.filter(project=selected_project)
            return render_to_response('reassign_project_select.html',{'user_name':user_name,'selected_project':selected_project,'employee_list':employee_list,'project':project},RequestContext(request))    
        else:
            return render_to_response('reassign_project_select.html',{'user_name':user_name,'selected_project':selected_project,'employee_list':employee_list,'project':project},RequestContext(request))    
    else:
        return HttpResponseRedirect("/progazer/login/")

def leave_applicationn(request):
    optional = Optional_holidays.objects.all()
    user = request.user
    datee = date.today()
    employee_user = employee.objects.get(email=user)
    user_name = employee_user.firstname
    try:
        if emp_project.objects.filter(employee=employee_user.id,approver=1).count() != 0:
            user_status = '2'
        else:
            user_status = '0'
    except:
        user_status = '0'
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        user_status = '3'
    if user.is_staff and user.is_superuser:
        user_status = '1'
    if user.is_active and user.is_staff:
        user_name = employee_user.firstname
        employee_user_id = employee_user.id
        application_list = Leave_application.objects.filter(employee=employee_user,approved=0).order_by('-id')
        application_list_approved = Leave_application.objects.filter(employee=employee_user,approved=1)
        application_list_rejected = Leave_application.objects.filter(employee=employee_user,approved=2)
        employee_name = employee_user.firstname+" "+employee_user.lastname
        if request.method=='POST':
            if 'new' in request.POST:
                form = Leave_applicationForm()
                return render_to_response('leave_application.html',{'optional':optional,'user_name':user_name,'user_status':user_status,'form':form,'employee_name':employee_name,'application_date':datee},RequestContext(request))
            else:
                pass
            leave_start_date = request.POST['start_date']
            leave_end_date = request.POST['end_date']
            try:
                choices = request.POST['choices']
                pass
            except:
                choices = '3'
                pass
            leave_type = Leave_type.objects.get(id=request.POST['leave_type'])
            leave_type_mail = leave_type.type
            remarks = request.POST['remarks']
            print leave_start_date,leave_end_date,choices,leave_type
            try:
                Leave_application.objects.get(employee=employee_user,date_of_application=datee,leave_start_date=leave_start_date,leave_end_date=leave_end_date,leave_type=leave_type,Choices=choices)
                return HttpResponse("Leave already Applied")
            except:
                pass
            token = hashlib.md5(str(datetime.now().isoformat())).hexdigest()
            Leave_application.objects.create(employee=employee_user,date_of_application=datee,leave_start_date=leave_start_date,leave_end_date=leave_end_date,leave_type=leave_type,Choices=choices,remarks=remarks,token=token)
            employee_reporter = employee_user.reporting_person
            new_application = Leave_application.objects.get(token=token)
            application_id = new_application.id 
            try:
                reporter = employee.objects.get(id=employee_reporter)
                if choices=='3':
                    day = "Full Day"
                else:
                    if choices=='2':
                        day ="Evening"
                    else:
                        if choices=='1':
                            day="Morning"
                message = "hello "+employee_name+" has applied for a leave from date "+leave_start_date+" to "+leave_end_date+" "+day+" due to "+leave_type_mail+" .Remarks ( "+remarks+" ).To approve the leave click on http://115.248.233.133:8989/progazer/leave_approver/"+token+"/"
                subject = "Leave Application of "+employee_name
                print message
                send_mail(subject,message,"ProGazer@ProGazer.com",[reporter.email])
            except:
                pass 
            projects = emp_project.objects.filter(employee=employee_user_id)
            for project_list in projects:
                project_id = project_list.project.id
                project_name = project_list.project.name
                project = Project.objects.get(id=project_id) 
                list_of_project_approver = emp_project.objects.filter(approver=1,project=project)
                for email_list in list_of_project_approver:
                    employee_list = email_list.employee.email
                    print choices
                    if choices=='3':
                        dayy = "Full Day"
                    else:
                        if choices=='2':
                            dayy ="Evening"
                        else:
                            if choices=='1':
                                dayy="Morning"
                    message = "hello "+employee_name+" working on project "+project_name+" has applied for a leave from date "+leave_start_date+" to "+leave_end_date+" "+dayy+" due to "+leave_type_mail+" .Remarks ("+remarks+" )"
                    subject = "Leave Application of "+employee_name
                    send_mail(subject,message,"ProGazer@ProGazer.com",[employee_list])
            form = Leave_applicationForm()
            return HttpResponseRedirect('progazer/leave_application/')
        else:
            return render_to_response('leave_register.html',{'user_name':user_name,'user_status':user_status,'user_name':user_name,'application_list':application_list,'application_list_approved':application_list_approved,'application_list_rejected':application_list_rejected},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def leave_application_editt(request,token):
    user = request.user
    employee_user = employee.objects.get(email=user)
    try:
        if emp_project.objects.filter(employee=employee_user.id,approver=1).count() != 0:
            user_status = '2'
        else:
            user_status = '0'
    except:
        user_status = '0'
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        user_status = '3'
    if user.is_staff and user.is_superuser:
        user_status = '1'
    
    if user.is_active and user.is_staff:
        try:
            application = Leave_application.objects.get(token=token,status=2)
            return HttpResponse("Leave application cancelled")
        except:
            pass
        application = Leave_application.objects.get(token=token)
        form = Leave_applicationForm(instance=application)
        employee_id = application.employee.id
        employee_requester = employee.objects.get(id=employee_id)
        employee_name = employee_requester.firstname+" "+employee_requester.lastname
        application_date = application.date_of_application
        start_date =application.leave_start_date
        end_date = application.leave_end_date
        ch = application.Choices
        remarks = application.remarks
        if (ch=='1'):
            choices='Morning'
        else:
            if (ch=='2'):
                choices='Evening'
            else:
                choices='Full Day'
        leave_type = application.leave_type
        if request.method=='POST':
            if 'cancel' in request.POST:
                Leave_application.objects.filter(token=token).update(status=2)
                print "cancel"
                return HttpResponseRedirect("/progazer/leave_application/")
        else:
        
            return render_to_response('leave_application_edit.html',{'user_status':user_status,'form':form,'remarks':remarks,'leave_type':leave_type,'choices':choices,'start_date':start_date,'end_date':end_date,'employee_name':employee_name,'application_date':application_date,'form':form},RequestContext(request))

    else:
        return HttpResponseRedirect("/progazer/login/")

def leave_approverr(request,token):
    user = request.user
    if user.is_active and user.is_staff:
        try:
            Leave_application.objects.get(token=token,status=2)
            return HttpResponse("Employee has cancelled the leave application")
        except:
            pass
        try:
            Leave_application.objects.get(token=token,status=1,approved=1)
            return HttpResponse("Application already approved")
        except:
            pass
        try:
            Leave_application.objects.get(token=token,status=2,approved=2)
            return HttpResponse("Application Rejected")
        except:
            pass
        application = Leave_application.objects.get(token=token)
        application_id = str(application.id)
        form = Leave_applicationForm( instance=application )
        employee_id = application.employee.id
        employee_requester = employee.objects.get(id=employee_id)
        employee_name = employee_requester.firstname+" "+employee_requester.lastname
        application_date = application.date_of_application
        start_date =application.leave_start_date
        end_date = application.leave_end_date
        ch = application.Choices
        remarks = application.remarks
        approver_remarks = application.approver_remarks
        if (ch=='1'):
            choices='Morning'
        else:
            if (ch=='2'):
                choices='Evening'
            else:
                choices='Full Day'
        leave_type = application.leave_type
        pop = '2'
        try:
            reporter_id = employee_requester.reporting_person
            reporter_employee = employee.objects.get(id=reporter_id)
            if (user.username == reporter_employee.email):
                if request.method=='POST':
                    if 'approve' in request.POST:
                        approver_remarks = request.POST['approver_remarks']
                        Leave_application.objects.filter(token=token).update(approved=1,approved_by=reporter_id,approver_remarks=approver_remarks)
                        message = "Hello, Your leave application with ID"+application_id+" is approved. Approver Remarks ("+approver_remarks+" )."
                        subject = "Leave Application ID: "+application_id+" Approved"
                        send_mail(subject,message,"progazer@progazer.com",[employee_requester.email])
                        pop = '3'
                        return render_to_response('leave_approver.html',{'approverremarks':approver_remarks,'popup':pop,'remarks':remarks,'leave_type':leave_type,'choices':choices,'start_date':start_date,'end_date':end_date,'employee_name':employee_name,'application_date':application_date,'form':form},RequestContext(request))
                    if 'reject' in request.POST:
                        approver_remarks = request.POST['approver_remarks']
                        Leave_application.objects.filter(token=token).update(approved=2,approved_by=reporter_id,approver_remarks=approver_remarks)
                        message = "Hello, Your leave application with ID"+application_id+" is rejected. Approver Remarks ("+approver_remarks+" )."
                        subject = "Leave Application ID: "+application_id+" Rejected"
                        send_mail(subject,message,"progazer@progazer.com",[employee_requester.email])
                        pop = '4'
                        return render_to_response('leave_approver.html',{'approverremarks':approver_remarks,'popup':pop,'remarks':remarks,'leave_type':leave_type,'choices':choices,'start_date':start_date,'end_date':end_date,'employee_name':employee_name,'application_date':application_date,'form':form},RequestContext(request))
                else:
                    return render_to_response('leave_approver.html',{'approverremarks':approver_remarks,'popup':pop,'remarks':remarks,'leave_type':leave_type,'choices':choices,'start_date':start_date,'end_date':end_date,'employee_name':employee_name,'application_date':application_date,'form':form},RequestContext(request))
            else:
                return render_to_response('leave_approver.html',{'popup':pop,'remarks':remarks,'leave_type':leave_type,'choices':choices,'start_date':start_date,'end_date':end_date,'employee_name':employee_name,'application_date':application_date,'form':form},RequestContext(request))
        except:
            return render_to_response('leave_approver.html',{'approverremarks':approver_remarks,'popup':pop,'remarks':remarks,'leave_type':leave_type,'choices':choices,'start_date':start_date,'end_date':end_date,'employee_name':employee_name,'application_date':application_date,'form':form},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")

def generate_passwordd(request):
    if request.method=='POST':
        email = request.POST['email']
        if User.objects.filter(username__exact=email).exists():
            return render_to_response('new_user.html',{'pop':'1'},RequestContext(request))
        else:
            if employee.objects.filter(email=email).exists():
                username = email
                password = User.objects.make_random_password()
                user = User.objects.create_user(username,email,password)
                user.is_staff = True
                user.is_active = True
                user.save()
                message = "your password is "+password +" and login id is " +email
                send_mail("login details",message,"ProGazer@ProGazer.com",[email])
                return render_to_response('new_user.html',{'pop':'2'},RequestContext(request))
            else:
                return render_to_response('new_user.html',{'pop':'3'},RequestContext(request))
            
    else:
        return render_to_response('new_user.html',{'pop':'0'},RequestContext(request))       

# import csv is not an error

import csv   
from testpro.settings import MEDIA_ROOT
def attendence_entry(request):
    if request.user.is_active and (request.user.groups.filter(id=2).count()!=0):
        if request.user.groups.filter(id=1).count()!=0:
            user_status=1
        else:
            user_status=2
        logger = employee.objects.get(email=request.user)
        user_name = logger.firstname
        form = AttendenceForm()
        if request.method=='POST':
            form = AttendenceForm(request.POST,request.FILES)
            if request.FILES == {}:
                return render_to_response('attendence.html',{'user_status':user_status,'user_name':user_name,'form':form},RequestContext(request))
    
            else:
                pass
            paramFile = request.FILES['dd'].read()
            p= MEDIA_ROOT+"temp_csv/att.csv"
            fo = open(p,"w+")
            fo.write(paramFile)
            fo.close()
            csv_data = csv.reader(file(p),delimiter='\t')
            error_list1 = []
            error_list2 = []
            for row in csv_data:
                date = row[0]
                print row[2]
                in_time = row[10]
                out_time = row[11]
                duration = row[12]
                i=2
                employees = employee.objects.all()
                for x in employees:
                    z = x.firstname.lower()+x.lastname.lower()
                    if row[2].lower() == z:
                        print x.id
                        name = employee.objects.get(id=x.id)
                        try:
                            Attendence.objects.get(date=date,employee=name)
                            i=0
                            print i
                            error_list1.append(row)
                            print error_list1
                            break
                        except:
                            try:
                                Attendence.objects.create(duration=duration,date=date,employee=name,in_time=in_time,out_time=out_time)
                                print "inserted"
                                i=1
                                break
                            except:
                                i=2
                if i==2:
                    error_list2.append(row)
                    
            return render_to_response('attendence.html',{'user_status':user_status,'user_name':user_name,'error_list2':error_list2,'error_list1':error_list1,'form':form},RequestContext(request))
        else:
            return render_to_response('attendence.html',{'user_status':user_status,'user_name':user_name,'form':form},RequestContext(request))
    else:
        return HttpResponseRedirect("/progazer/login/")
    
def view_attendence_emp(request):
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        user_name = employee.objects.get(email=request.user).firstname
        employee_list = employee.objects.all().order_by('firstname')
        return render_to_response('view_attendence_emp.html',{'selected_employee':"",'employee_list':employee_list,'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect('/progazer/login/')
    
def view_attendence_employee(request,employee_id,year_s,month_s,day_s,year_e,month_e,day_e):
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        start_date = year_s+"-"+month_s+"-"+day_s
        user_name = employee.objects.get(email=request.user).firstname
        end_date = year_e+"-"+month_e+"-"+day_e
        selected_employee = employee.objects.get(id=employee_id)
        emp_attend = Attendence.objects.filter(employee=selected_employee,date__range=[start_date,end_date]).order_by('date')
        total_time = []
        for emp in emp_attend:
            out = datetime.combine(date.today(), emp.out_time)
            in_t = datetime.combine(date.today(), emp.in_time)
            time = out - in_t 
            total_time.append(time)
        print total_time
        user_name = employee.objects.get(email=request.user).firstname
        employee_list = employee.objects.all().order_by('firstname')
        return render_to_response('view_attendence_emp.html',{'user_name':user_name,'start_date':start_date,'end_date':end_date,'total_time':total_time,'emp_attend':emp_attend,'selected_employee':selected_employee,'employee_list':employee_list,'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect('/progazer/login/')
    
def view_attendence_without_date(request):
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        user_name = employee.objects.get(email=request.user).firstname
        return render_to_response('view_attendence_date.html',{'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect('/progazer/login/')
def view_attendence_date(request,year,month,day):
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        user_name = employee.objects.get(email=request.user).firstname
        date = year+"-"+month+"-"+day
        emp_attend = Attendence.objects.filter(date=date).order_by('employee')
        return render_to_response('view_attendence_date.html',{'user_name':user_name,'date':date,'emp_attend':emp_attend},RequestContext(request))
    else:
        return HttpResponseRedirect('/progazer/login/')

def manage_hr(request):
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        user_name = employee.objects.get(email=request.user).firstname
        hr_user = User.objects.filter(groups=1)
        employee_list = employee.objects.all()
        k =[]
        for d in hr_user:
            k.append(d.username)
        if request.method=='POST':
            if 'remove' in request.POST:
                email = request.POST['e_user']
                user = User.objects.get(username=email)
                g = Group.objects.get(name='HR') 
                g.user_set.remove(user)
                hr_user = User.objects.filter(groups=1)
                employee_list = employee.objects.all()
                return HttpResponseRedirect('/progazer/manage_hr/') #render_to_response('manage_hr.html',{'hr_user':k,'employee_list':employee_list,'user_name':user_name},RequestContext(request))
            if 'add' in request.POST:
                email = request.POST['e_user']
                try:
                    user = User.objects.get(username=email)
                    g = Group.objects.get(name='HR') 
                    g.user_set.add(user)
                    return HttpResponseRedirect('/progazer/manage_hr/')
                except:
                    return render_to_response('manage_hr.html',{'pop':'1','hr_user':k,'employee_list':employee_list,'user_name':user_name},RequestContext(request)) 
        return render_to_response('manage_hr.html',{'hr_user':k,'employee_list':employee_list,'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect('/progazer/login/')    

def manage_att_uploader(request):
    if request.user.is_active and (request.user.groups.filter(id=1).count()!=0):
        user_name = employee.objects.get(email=request.user).firstname
        attendence_user = User.objects.filter(groups=2)
        employee_list = employee.objects.all()
        k =[]
        for d in attendence_user:
            k.append(d.username)
        if request.method=='POST':
            if 'remove' in request.POST:
                email = request.POST['e_user']
                user = User.objects.get(username=email)
                g = Group.objects.get(name='Attendence uploader') 
                g.user_set.remove(user)
                attendence_user = User.objects.filter(groups=1)
                employee_list = employee.objects.all()
                return HttpResponseRedirect('/progazer/manage_att_uploader/') #render_to_response('manage_hr.html',{'hr_user':k,'employee_list':employee_list,'user_name':user_name},RequestContext(request))
            if 'add' in request.POST:
                email = request.POST['e_user']
                try:
                    user = User.objects.get(username=email)
                    g = Group.objects.get(name='Attendence uploader') 
                    g.user_set.add(user)
                    return HttpResponseRedirect('/progazer/manage_att_uploader/')
                except:
                    return render_to_response('manage_attendence.html',{'pop':'1','hr_user':k,'employee_list':employee_list,'user_name':user_name},RequestContext(request)) 
        return render_to_response('manage_attendence.html',{'hr_user':k,'employee_list':employee_list,'user_name':user_name},RequestContext(request))
    else:
        return HttpResponseRedirect('/progazer/login/')
    
def employee_upload(request):
    user_name = employee.objects.get(email=request.user)
    form = AttendenceForm()
    if request.method=='POST':
        form = AttendenceForm(request.POST,request.FILES)
        if request.FILES == {}:
            return render_to_response('emp_upload.html',{'user_name':user_name,'form':form},RequestContext(request))
        else:
            pass
        paramFile = request.FILES['dd'].read()
        p= MEDIA_ROOT+"temp_csv/att.csv"
        fo = open(p,"w+")
        fo.write(paramFile)
        fo.close()
        csv_data = csv.reader(file(p))
        error_list1 = []
        error_list2 = []
        for row in csv_data:
            try:
                old_id = row[0]
                units = unit.objects.get(unit=row[1])
                dob = row[3]
                doj = row[4]
                levels = level.objects.get(level=row[5])
                desig = Designations.objects.get(designation=row[6])
                dept = Department.objects.get(department=row[7])
                loc = location.objects.get(location=row[8])
                email = row[9]
                contact = row[10]
                name = row[2].split()
                if len(name)==2:
                    fn = name[0]
                    ln = name[1]        
                else:
                    pass
                if len(name)==3:
                    fn = name[0]+" "+name[1]
                    ln = name[2]    
                else:
                    pass
                if len(name)==4:
                    fn = name[0]+" "+name[1]+" "+name[2]
                    ln = name[3]    
                try:
                    employee.objects.get(firstname=fn,lastname=ln,dateofbirth=dob)
                    error_list1.append(row)
                except:
                    try:
                        employee.objects.create(unit=units,old_employee_id=old_id,firstname=fn,lastname=ln,dateofbirth=dob,dateofjoining=doj,level=levels,designation=desig,department=dept,email=email,location=loc,phone=contact)
                    except Exception,e:
                        error_list2.append(e)
            except Exception,e:
                error_list2.append(row)
                error_list2.append(e)
        return render_to_response('emp_upload.html',{'error_list1':error_list1,'error_list2':error_list2,'user_name':user_name,'form':form},RequestContext(request))
    else:
        return render_to_response('emp_upload.html',{'user_name':user_name,'form':form},RequestContext(request))
            
    