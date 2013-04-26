from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testpro.views.home', name='home'),
    # url(r'^testpro/', include('testpro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^employee_upload/?','testapp.views.employee_upload'),
    url(r'^optional_holiday/?','testapp.views.optional_holiday'),
    url(r'^manage_hr/?','testapp.views.manage_hr'),
    url(r'^manage_att_uploader/?','testapp.views.manage_att_uploader'),
    url(r'^view_attendence_date/?','testapp.views.view_attendence_without_date'),
    url(r'^view_attendence_with_date/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$','testapp.views.view_attendence_date'),
    
    url(r'^view_attendence_employee/(?P<employee_id>\d+)/(?P<year_s>\d{4})-(?P<month_s>\d{2})-(?P<day_s>\d{2})/(?P<year_e>\d{4})-(?P<month_e>\d{2})-(?P<day_e>\d{2})/$','testapp.views.view_attendence_employee'),
    url(r'^view_attendence_emp/?','testapp.views.view_attendence_emp'),
    url(r'^attendence/?','testapp.views.attendence_entry'),
    url(r'^generate_password/?','testapp.views.generate_passwordd'),
    url(r'^change_password/?','testapp.views.change_passwordd'),
    url(r'^login/?','testapp.views.loginn'),
    url(r'^admin_home/','testapp.views.admin_home_page'),
    url(r'^admin_home_hr/','testapp.views.admin_home_page_hr'),
    url(r'^leave_register_hr/','testapp.views.leave_register_hr'),
    url(r'^view_employee/','testapp.views.employee_view'),
    url(r'^view_employee_sorted/(?P<element>\d+)','testapp.views.employee_view_sorted'),
    url(r'^view_employeeid/(?P<employee_id>\d+)/$','testapp.views.employee_view_id'),
    url(r'^employee/','testapp.views.employeee'),
  #  url(r'^projecttype/','testapp.views.projecttypee'),
    url(r'^addclient/','testapp.views.addclientt'),
    url(r'^view_client/','testapp.views.view_clientt'),
    url(r'^view_clientid/(?P<client_id>\d+)/$','testapp.views.client_view_id'),
    url(r'^addproject/','testapp.views.addprojectt'),
    url(r'^view_project/','testapp.views.view_projectt'),
    url(r'^view_projectid/(?P<project_id>\d+)/$','testapp.views.project_view_id'),
    url(r'^addtimesheet/','testapp.views.addtimesheett_withoutdate'),
    url(r'^addtimesheett/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$','testapp.views.addtimesheett'),
   # url(r'^edittimesheet/(?P<time_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$','testapp.views.editt'),
  #  url(r'^submittimesheet/(?P<time_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$','testapp.views.subtimesheet'),
    url(r'^logout/?','testapp.views.logoutuser'),
    url(r'^forgotpassword/','testapp.views.forgotpswrd'),
    url(r'^viewtimesheet/','testapp.views.viewtimesheett_pre'),
    url(r'^viewtimesheetts/(?P<project_id>\d+)/$','testapp.views.viewtimesheett_pre_withproject'),
    url(r'^viewtimesheets/(?P<project_id>\d+)/(?P<employee_id>\d+)/$','testapp.views.viewtimesheett'),
 #   url(r'^approval_timesheet/(?P<record_id>\d+)/$','testapp.views.approval_timesheett'),
  #  url(r'^discard_timesheet/(?P<record_id>\d+)/$','testapp.views.discard_timesheett'),
    url(r'^client_project/','testapp.views.client_projectt'),
    url(r'^client_project_timesheets/(?P<project_id>\d+)/$','testapp.views.client_project_timesheett'),
    url(r'^assign_project/','testapp.views.assign_projectt'),
    url(r'^assign_projectt/(?P<project_id>\d+)/(?P<department_id>\d+)/(?P<unit_id>\d+)/$','testapp.views.assign_projectt_projectid'),
    url(r'^re_assign_project/','testapp.views.re_assign_projectt'),
    url(r'^re_assign_projectt/(?P<project_id>\d+)/','testapp.views.re_assign_project_with_id'),
    url(r'^leave_application/','testapp.views.leave_applicationn'),
    url(r'^leave_application_edit/(?P<token>[a-z0-9]{32})/$','testapp.views.leave_application_editt'),
    url(r'^leave_approver/(?P<token>[a-z0-9]{32})/$','testapp.views.leave_approverr'),
    url(r'^view_leave_hr_id/(?P<token>[a-z0-9]{32})/$','testapp.views.view_leave_hr_id')
    
 )
    