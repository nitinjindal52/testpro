#from django.conf.urls.defaults import *
#from tastypie.api import Api
#from apiapp.resource import UserResource
#from django.conf.urls import patterns, include, url
#
#
#user_api = Api()
#user_api.register(UserResource())
#
#urlpatterns = patterns('',
#                       (r'^user/', include(user_api.urls)),
##                       (r'^login/', include(login.urls)),
#                    )
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from api.handlers import TimesheetHandler,UserHandler,LeaveHandler

auth = HttpBasicAuthentication()
ad = { 'authentication': auth}


class CsrfExemptResource(Resource):
            """A Custom Resource that is csrf exempt"""
            def __init__(self, handler, authentication=None):
                super(CsrfExemptResource, self).__init__(handler, authentication)
                self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)
                
timesheet = CsrfExemptResource(handler=TimesheetHandler)
user = CsrfExemptResource(handler=UserHandler)
leave = CsrfExemptResource(handler=LeaveHandler)

urlpatterns = patterns('',
                       url(r'^user/timesheet/$', timesheet),
                       url(r'^user/leave/$', leave),
                       url(r'^user/$', user),
                       )