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
        certificates = Certificate.objects.filter(certificate_type__contains=searched)
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


def register_consultant(request):
    
    range_one = rate_range
    range_list=[]
    for i in range_one:
        range_list.append(i[0])

    current_user = request.user
    company_list=[]
    temp=[]
    company_dict=Company.objects.values('name')
    for item in company_dict:
        for key in item:
            temp.append(item[key])
    for i in temp:
        if i not in company_list:
            company_list.append(i)
    
    regions = []
    for key, value in regions_dictionary.items():
        regions.append(key)

    if current_user.is_authenticated and Profile.objects.get(user=current_user).profile_type=="Consultant":
        if request.method == "POST":
            region = request.POST.get('region')
            district = request.POST.get('district')
            rate = request.POST.get('rate')
            company = request.POST.get('company')

            if Company.objects.filter(name=company).exists():
                cmpny = Company.objects.get(name=company)
            else:
                cmpny = None
            phone_nmr = Profile.objects.get(user=current_user).phone_number

            consultant = Consultant(user_id = current_user, consultant_company = cmpny, region = region, district = district, rate_range = rate, name = str(current_user.first_name) + " " + str(current_user.last_name), phone_number = phone_nmr)
            consultant.save()
            return redirect('certificate')
        else:
            return render(request, 'SubHazApp/authenticate/register_consultant.html', {'range_list':range_list, 'company_list':company_list, 'certificate_types':certificate_types, 'regions_dictionary':regions_dictionary, 'regions':regions, })
    else:
        messages.success(request, ("You need to register a consultant profile first!"))
        return redirect('register')


def register_company(request):
    current_user = request.user
    if current_user.is_authenticated and Consultant.objects.filter(user_id=current_user).exists():
        if request.method == "POST":
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            fein = request.POST.get('fein')
            auth = Consultant.objects.get(user_id=current_user)

            company = Company(name=name, phone_number=phone,address=address,FEIN=fein, auth_consultant=auth)
            company.save()

            auth.consultant_company = company
            auth.save()

            messages.success(request, ("You have successfully registered your company!"))
            return redirect('home')

        else:
            return render(request, 'SubHazApp/authenticate/register_company.html')
    else:
        messages.success(request, ("You need to register a consultant profile first!"))
        return redirect('register')



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

def choice(request):
    return render(request, 'SubHazApp/authenticate/choice.html')

def certificate(request):
    current_user = request.user
    if current_user.is_authenticated and Consultant.objects.filter(user_id=current_user).exists():
        certificate_list = certificate_types
        certificate_list_len = len(certificate_list)
        length = 1
        if request.method == "POST":
            consultant = Consultant.objects.get(user_id=current_user)
            for number in range(1, 100):
                string = "certificate"+str(number)
                if request.POST.get(string) is not None:
                    length = number

            for cert in range(1, length+1):
                string1 = 'certificate'+str(cert)
                string2 = 'expiration_date'+str(cert)
                string3 = 'image'+str(cert)

                certificate_type = request.POST.get(string1)
                expiration_date = request.POST.get(string2)
                image = request.FILES.get(string3)

                certificate = Certificate(consultant_Id=consultant, certificate_type=certificate_type, expiration_date=expiration_date, image=image)
                certificate.save()

            messages.success(request, ("We are now validating your profile."))
            return redirect('home')
        else:
            return render(request, 'SubHazApp/authenticate/certificate.html', {'certificate_list':certificate_list, 'certificate_list_len':certificate_list_len, })
    else:
        messages.success(request, ("You need to register a consultant profile first!"))
        return redirect('register')


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

def upload_file(request):
	if "GET" == request.method:
		return render(request, 'SubHazApp/uploadfile.html', {})
	else:
		Certificate.objects.all().delete()
		Company.objects.all().delete()
		Consultant.objects.all().delete()
		excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

		wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
		worksheet = wb["Sheet1"]
		print(worksheet)

		excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
		for row in worksheet.iter_rows():
			row_data = list()
			for cell in row:
				row_data.append(str(cell.value))
			excel_data.append(row_data)
		#adding  to db
		for row in excel_data:
			# skip empty recorrds
			if row[1] =="None" or row[1] == "Last name":
				continue
			# if is affiliated
			isaffiliated = False
			if row[3] != "None":
				company_name = row[3]
				if Company.objects.filter(name = company_name).exists():
					company = Company.objects.get(name = company_name)
				else:
					company = Company.objects.create(name = company_name)
					company.save
				isaffiliated = True
			first_name = row[2]
			last_name = row[1]
			name = first_name + " " + last_name
			certificate_type = row[0]
			city = row[4]
			telephone = row[5]
			if Consultant.objects.filter(name = name, phone_number = telephone).exists():
				continue
			consultant = Consultant.objects.create(name = name, phone_number = telephone, region = city)
			consultant.save
			if isaffiliated:
				consultant.consultant_company = company
			certificate = Certificate.objects.create(certificate_type = certificate_type, consultant_Id = consultant, expiration_date = datetime.datetime(2023, 5, 17))
			certificate.save

		return render(request, 'SubHazApp/uploadfile.html', {"excel_data":excel_data})
