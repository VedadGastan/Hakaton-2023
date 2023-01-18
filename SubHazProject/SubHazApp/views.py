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

cities_list = ["Sarajevo", "Tuzla", "Zenica","Mostar", "Banja Luka"]

def search(request):
    if request.method == "POST":
        results = []
        searched = request.POST.get('searched')
        profiles = Profile.objects.filter(city__contains=searched)
        for profile in profiles:
            if profile.city == searched and profile.status==1:
                results.append(profile)


        return render(request, 'SubHazApp/work.html', {'searched' : searched, 'results':results, 'cities_list' : cities_list, })
    else:
        return render(request, 'SubHazApp/work.html', {'cities_list' : cities_list,})




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

def about(request):
    return render(request, 'SubHazApp/about.html')

def contact(request):
    return render(request, 'SubHazApp/contact.html')

def client(request):
    return render(request, 'SubHazApp/client.html')


def contractors(request):
    profiles = []
    profiles_all = Profile.objects.all()
    for profile in profiles_all:
        if profile.status == 1:
            profiles.append(profile)

    return render(request, 'SubHazApp/contractors.html', {'profiles':profiles})



def job_offers(request):
    return render(request, 'SubHazApp/job-offers.html')

def work(request):
    return render(request, 'SubHazApp/work.html')


def blog(request):
    posts = Post.objects.all()
    return render(request, 'SubHazApp/blog.html', {'posts':posts})


def post_details(request, slug):
    posts = Post.objects.all()
    post = Post.objects.get(slug=slug)
    return render(request, 'SubHazApp/blog-inner.html', {'post':post, 'posts':posts})
