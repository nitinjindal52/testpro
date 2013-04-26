# Create your views here.
from apiapp.resource import UserResource
from tastypie.authorization import DjangoAuthorization

def user_login(request):
    user_res = UserResource()
    user = user_res.obj_get(request.POST)
    if 