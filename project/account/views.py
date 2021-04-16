from django.shortcuts import render, redirect, reverse
import urllib
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from account.models import User

def custom_redirect(url_name, *args, **kwargs):
    import urllib
    url = reverse(url_name, args = args)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

def login_user(request):
    logtype = 'student'
    try:
        logtype = request.GET['type']
    except:
        pass
    return login_user_func(request, logtype)

def login_user_func(request, logtype='student'):
    user_map = {
        False:'student',
        True: 'admin'
    }
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        message = ''
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            remember_user = 0
            try:
                remember_user = request.POST["rememberme"]
            except:
                pass
            if not remember_user:
                request.session.set_expiry(0)
                request.session.modified = True
            user = authenticate(request, email=email, password=password)
            user_m = User.objects.get(pk=user.pk)
            if user is not None:
                if user_map[user_m.is_admin] == logtype:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return custom_redirect('user-login', type=user_map[user_m.is_admin])
            else:
                message = "Invalid Credentials. Try again!"
        return render(request, f'{logtype}_dashboard/login.html', context={'message':message, 'title': "Face AMS - Student Login"})
