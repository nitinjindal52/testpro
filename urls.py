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
    
     url(r'^api/', include('api.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^progazer/',include('testapp.urls')),
#     url(r'^index/','testapp.views.index'),
#     url(r'^login/?','testapp.views.loginn'),
#     url(r'^employee/','testapp.views.employeee'),
#     url(r'^projecttype/','testapp.views.projecttypee'),
#     url(r'^addclient/','testapp.views.addclientt'),
#     url(r'^addproject/','testapp.views.addprojectt'),
#     url(r'^addtimesheet/','testapp.views.addtimesheett_withoutdate'),
#     url(r'^addtimesheett/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$','testapp.views.addtimesheett'),
#     url(r'^edittimesheet/(?P<time_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$','testapp.views.editt'),
#     url(r'^submittimesheet/(?P<time_id>\d+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$','testapp.views.subtimesheet'),
#     url(r'^logout/?','testapp.views.logoutuser'),
#     url(r'^forgotpassword/','testapp.views.forgotpswrd'),
#     url(r'^viewtimesheet/','testapp.views.viewtimesheett_pre'),
#     url(r'^viewtimesheetts/(?P<project_id>\d+)/$','testapp.views.viewtimesheett_pre_withproject'),
#     url(r'^viewtimesheets/(?P<project_id>\d+)/(?P<employee_id>\d+)/$','testapp.views.viewtimesheett'),
#     url(r'^approval_timesheet/(?P<record_id>\d+)/$','testapp.views.approval_timesheett'),
#     url(r'^discard_timesheet/(?P<record_id>\d+)/$','testapp.views.discard_timesheett'),
#     url(r'^client_project/(?P<client_id>\d+)/$','testapp.views.client_projectt'),
#     url(r'^client_project_timesheets/(?P<project_id>\d+)/$','testapp.views.client_project_timesheett'),
# 
 # urls of api
    
 
 
     
 )
