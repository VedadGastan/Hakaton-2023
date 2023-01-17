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

regions_dictionary = {

    "Fair Oaks": ["District1", "District2", "District3"],
    "Virginia Beach": ["District1", "District2", "District3"],

}

def search(request):

    regions=[]
    temp=[]
    regions_dict=Consultant.objects.values('region')

    for item in regions_dict:
        for key in item:
            temp.append(item[key])

    for i in temp:
        if i not in regions:
            regions.append(i)

    if request.method == "POST":
        results = []
        searched = request.POST.get('searched')
        searched_region = request.POST.get('searched_region')
        searched_district = request.POST.get('searched_district')
        certificates = Profile.objects.filter(certificate_type__contains=searched)
        for cert in certificates:
            if cert.consultant_Id.region == searched_region and cert.consultant_Id.district == searched_district and cert.status==1:
                results.append(cert)


        return render(request, 'SubHazApp/search.html', {'searched' : searched, 'results':results, 'regions' : regions, 'searched_region':searched_region, 'certificate_types':certificate_types, 'regions_dictionary':regions_dictionary, })
    else:
        return render(request, 'SubHazApp/search.html', {'regions' : regions, 'certificate_types':certificate_types, 'regions_dictionary':json.dumps(regions_dictionary), })




def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        profile_type = request.POST['profile_type']
        user = authenticate(request, username=username, password=password)
        if profile_type == 'consultant' and user is None:
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
        form2 = RegisterProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            profile_type = form2.cleaned_data['profile_type']


            onetoone = form2.save(commit=False)
            onetoone.user = user
            form2.save()

            name = str(first_name) + " " + str(last_name)

            consultants=Consultant.objects.all()
            login(request, user)
            if profile_type == 'Consultant':
                for consultant in consultants:
                    if consultant.name == name:
                        consultant.user_id = user
                        consultant.save()
                if not Consultant.objects.filter(name=name).exists():
                    return redirect('register_consultant');
            
            messages.success(request, ("You have signed up successfully!"))
            return redirect('home')
    else:
        form1 = RegisterUserForm
        form2 = RegisterProfileForm

    return render(request, 'SubHazApp/authenticate/register.html', {'form1':form1, 'form2':form2, })



def unavailability(request):
    current_user = request.user
    if current_user.is_authenticated and Consultant.objects.filter(user_id=current_user).exists():
        if request.method == "POST":

            busy_from = request.POST.get('busy_from')
            busy_until = request.POST.get('busy_until')
            consultant = Consultant.objects.get(user_id=current_user)
            if busy_from > busy_until:
                messages.success(request, ("Invalid dates, try again"))
                return render(request, 'SubHazApp/authenticate/unavailability.html')
            else:
                unavailability = Unavailability(consultant_Id=consultant, busy_from=busy_from, busy_until=busy_until)
                unavailability.save()
                return redirect('contractor', name=consultant)
        else:
            return render(request, 'SubHazApp/authenticate/unavailability.html')

    else:
        messages.success(request, ("You need to login first"))
        return redirect('login')

def index(request):
    return render(request, 'SubHazApp/index.html')

def about(request):
    return render(request, 'SubHazApp/about.html')

def contact(request):
    return render(request, 'SubHazApp/contact.html')

def client(request):
    return render(request, 'SubHazApp/client.html')


def contractors(request):
    certificates = []
    certificates_all = Certificate.objects.all()
    for certificate in certificates_all:
        if certificate.status == 1:
            certificates.append(certificate)

    return render(request, 'SubHazApp/contractors.html', {'certificates':certificates})




delta = 0
def contractor(request, name):
    is_consultant = False
    current_user = request.user
    if current_user.is_authenticated and Consultant.objects.filter(user_id=current_user).exists():
        is_consultant = True

    contractor = Consultant.objects.get(name=name)
    unavailabilities = Unavailability.objects.filter(consultant_Id=contractor)
    if Certificate.objects.get(consultant_Id=contractor).status == 0:
        messages.success(request, ("We are still validating this account!"))
        return redirect('home')

    global delta
    
    if request.POST.get('Next') is not None:
        if len(request.POST.get('Next')) % 2 == 0:
            delta = delta + 1

    if request.POST.get('Previous') is not None:
        if len(request.POST.get('Previous')) % 2 != 0:
            delta = delta - 1

    now = datetime.datetime.now() + relativedelta.relativedelta(months=delta)

    weekday_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    year = now.year
    month = now.strftime("%B")
    first_day = now.replace(day=1)
    first_day_num = int(first_day.strftime("%w"))

    if first_day_num == 0:
        first_day_num = 7

    num_of_days = calendar.monthrange(year, now.month)[1]
    cal = []



    for i in range(1, first_day_num + 1):
        cal.append(['<td> </td>', None])

    for day in range(1, num_of_days+1):
        cal.append(['<td>'+str(day)+'</td>', int(day)])

    for day in cal:
        if isinstance(day[1], int):
            x = datetime.datetime(year, now.month, day[1]).date()
            if unavailabilities.exists():
                for unavailability in unavailabilities:
                    if x >= unavailability.busy_from and x <= unavailability.busy_until:
                        day[0] = '<td class="unavailable">'+str(day[1])+'</td>'

    return render(request, 'SubHazApp/contractor.html', {'contractor':contractor, 'year':year, 'month':month, 'weekday_list':weekday_list, 'cal':cal, 'is_consultant':is_consultant, 'delta':delta})



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
