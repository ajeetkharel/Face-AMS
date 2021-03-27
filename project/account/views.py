from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_user(request):
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
                print("Not remembering")
                request.session.set_expiry(0)
                request.session.modified = True
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                message = "Invalid Credentials. Try again!"
        return render(request, 'admin_dashboard/login.html', context={'message':message, 'title': "Face AMS - Admin Login"})

def register_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            return render(request, 'admin_dashboard/register.html', context={'form':form, 'title': "Register an Account"})
    return render(request, 'admin_dashboard/register.html', context={'title': "SabFood - Register"})
