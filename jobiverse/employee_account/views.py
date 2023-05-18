from django.shortcuts import get_object_or_404, render,redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
# from company.signals import create_job_application_notification
from.models import Employee,Profile_details
from company.models import Job_Application,Job_Vacancy,Company,Notification
from django.contrib.auth.decorators import login_required
from datetime import datetime
from custom_admin.models import User
from django.http import HttpResponse, Http404

from company.models import Job_Application
from .forms import JobApplicationForm
# Create your views here.

@login_required(login_url='signin')
def home(request):
    search = request.GET.get('search')
    page_number = request.GET.get('page',1)
    company = Company.objects.all()
    jobs = Job_Vacancy.objects.all().order_by('-posted')
    
    if search:
        jobs = jobs.filter(designation__icontains=search)
    job_application = Job_Application.objects.filter(employee = request.user.employee)
    li=[]
    for i in job_application:
       
        li.append(i.job_vacancy.id)
    count = len(li)


    paginator = Paginator(jobs,3)
    page = paginator.page(page_number)
    jobs = page.object_list
    
    context={
        'jobs':jobs,
        'company':company,
        'job_application':job_application,
        'li':li,
        'count':count,
        'pages':list(range(1,paginator.num_pages+1))
    }
    
    return render(request,'employee_account/home.html',context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        # dob = datetime.strptime(dob, '%Y-%m-%d').date()
        profile_img = request.FILES.get('p_image')
        resume = request.POST.get('resume')
        password = request.POST.get('password')
        re_password = request.POST.get('password2')

        if password == re_password:
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create_user(
                    first_name=f_name,
                    last_name=l_name,
                    username=username,
                    email=email,
                    password=password,
                    is_employee=True
                )
                Employee.objects.create(
                    user=user,
                    DOB=dob,
                    profile_img=profile_img,
                    email=email,
                    phone=phone,
                    resume=resume
                )
                messages.success(request, 'Account created successfully')
                return redirect('signin')
            else:
                messages.error(request, 'Account already exists')
        else:
            messages.error(request, 'Invalid password or credentials')

    return render(request,'employee_account/registeration.html')



@login_required(login_url='signin')
def employee_profile(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            profile = Profile_details.objects.filter(user=request.user.employee).first()
            context ={
                'employee':employee,
                'profile':profile
            }
            return render(request,'employee_account/emp_profile.html',context)
        except Employee.DoesNotExist:
            raise Http404('profile not exist')
    else:
        raise Http404('You are not authorized to this page')




# def sign_in(request):
#     if request.method == 'POST':
#         username = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(username = username,password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             messages.error(request,'no account found')
#         messages.error(request,'invalid credentials')   
#     return render(request,'employee_account/signin.html')


def sign_out(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def job_application_create(request,id):
    job_vacancy=Job_Vacancy.objects.get(id=id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.employee = request.user.employee 
            job_application.job_vacancy = job_vacancy
            job_application.save()
            # create_job_application_notification.send(sender=Job_Application, instance=job_application, created=True, request=request)

            messages.success(request, 'Job application submitted successfully.')
            return redirect('job_application_detail')
        
    else:
        form = JobApplicationForm()
    context = {
        "job_vacany":job_vacancy,
        "form":form,
        "request":request
    }    
    
    return render(request, 'employee_account/job_application_create.html', context)




@login_required(login_url='signin')
def job_application_detail(request):
    #job_application = get_object_or_404(Job_Application, id=id)
    job_application  = Job_Application.objects.filter(employee = request.user.employee)
   
    
    return render(request, 'employee_account/job_application_details.html', {'job_application': job_application})

@login_required(login_url='signin')
def employee_profile_edit(request):
    employee = request.user.employee
    profile = employee.profile_details_set.first()

    if request.method == 'POST':
        profile_img = request.FILES.get('edit_image')
        about = request.POST.get('about')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        education = request.POST.get('education')
        hobbies = request.POST.get('hobbies')
        
        employee.profile_img = profile_img
        employee.save()

        if not profile:
            profile = Profile_details(user=employee)
        
        profile.profile_img = profile_img
        profile.about = about
        profile.experience = experience
        profile.skills = skills
        profile.education = education
        profile.hobbies = hobbies
    
        profile.save()
        messages.success(request,'saved changes')
    

    context = {
        'profile': profile,
    }

    return render(request, 'employee_account/employee_profile_edit.html', context)



def my_jobs(request):
    employee = request.user.employee
    job_applications = Job_Application.objects.filter(employee=employee)
    notify = Notification.objects.filter(employee=employee)
    notifications =[]
    for i in job_applications:
        if i.status != 'submitted':
            notification = f"{i.job_vacancy} you have applied {i.status} by {i.job_vacancy.company} "
        notifications.append(notification)        
    context = {
        'job_applications': job_applications,
        'notifications': notifications,
       
        
    }
    return render(request, 'employee_account/notification_emp.html', context)
