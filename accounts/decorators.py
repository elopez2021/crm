from django.http import HttpResponse
from django.shortcuts import redirect


#a decorator is a function that takes in another function in as a paremeter and lets us add a little extra functionality before the original function is called


#decorator to restrict the user from viewing the register and login page
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
           return redirect('home')#if they are authenticated, they are gonna send back to the homepage. The use cannot see this page if they're logged in
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#the roles that gonna have each user
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Your are not authorized to view this page')
        return wrapper_func
    return decorator