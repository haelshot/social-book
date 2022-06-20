from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages, auth
from core.models import profile
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cPassword = request.POST['cPassword']
        email = request.POST['email']

        if password == cPassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('signup')
            else:
                user = User.objects.create(username=username, email=email, password=password)
                user.save()

                #log user in and redirect t0 settings page

                # create a profile object for each user
                user_model = User.objects.get(username=username)
                new_profile = profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'username or password invalid')
            return redirect('signin')
    
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')