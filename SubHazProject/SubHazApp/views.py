from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.shortcuts import render
import datetime
import openpyxl
import calendar
from dateutil import relativedelta
import json

cities_list = ["Sarajevo", "Zenica", "Tuzla", "Banja Luka", "Mostar"]

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect('register')

        else:
            if user is not None:
                login(request, user)
                messages.success(request, ("You logged in successfully!"))
                return redirect('home')
            else:
                messages.success(request, ("There was an error logging in, try again..."))
                return redirect('login')

    else:
        return render(request, 'SubHazApp/authenticate/login.html', {})



def logout_user(request):
    logout(request)
    messages.success(request, ("You logged out successfully!"))
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form1 = RegisterUserForm(request.POST)
        if form1.is_valid():
            form1.save()
            
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']

            city = request.POST.get('city')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            image = request.FILES.get('image')
            image_id = request.FILES.get('image_id')
            charge_rate = request.POST.get('charge_rate')
            description = request.POST.get('description')

            profile = Profile(user=user, city=city,phone_number=phone_number, address=address, image=image, image_id=image_id, charge_rate=charge_rate,description=description)
            profile.save()

            login(request, user)
            
            return redirect('home')
    else:
        form1 = RegisterUserForm

    return render(request, 'SubHazApp/authenticate/register.html', {'form1':form1, 'cities_list':cities_list})


def index(request):
    profiles = Profile.objects.all()
    return render(request, 'SubHazApp/index.html', {'profiles': profiles, })


def subscriptions(request):
    return render(request, 'SubHazApp/subscriptions.html')


def contractors(request):
    searched = 0
    profiles = Profile.objects.filter(status=1)
    if request.method == "POST":
        searched=1
        

        city = request.POST.get('searched')

        setac = request.POST.get('setac')
        cuvar = request.POST.get('cuvar')
        trener = request.POST.get('trener')

        if not setac and not cuvar and not trener:
            profiles = Profile.objects.filter(status=1, city=city)
        if setac and not cuvar and not trener:
            profiles = Profile.objects.filter(status=1, city=city).filter(setac=1)
        if cuvar and not setac and not trener:
            profiles = Profile.objects.filter(status=1, city=city).filter(cuvar=1)
        if trener and not setac and not cuvar:
            profiles = Profile.objects.filter(status=1, city=city).filter(trener=1)
        if trener and setac and not cuvar:
            profiles = Profile.objects.filter(status=1, city=city).filter(trener=1).filter(setac=1)
        if trener and cuvar and not setac:
            profiles = Profile.objects.filter(status=1, city=city).filter(trener=1).filter(cuvar=1)
        if setac and cuvar and not trener:
            profiles = Profile.objects.filter(status=1, city=city).filter(cuvar=1).filter(setac=1)
        if setac and cuvar and trener:
            profiles = Profile.objects.filter(status=1, city=city).filter(trener=1).filter(cuvar=1).filter(setac=1)


        return render(request, 'SubHazApp/members.html', {'profiles':profiles, 'cities_list':cities_list, 'searched':searched})
    else:
        return render(request, 'SubHazApp/members.html', {'profiles':profiles, 'cities_list':cities_list,'searched':searched})