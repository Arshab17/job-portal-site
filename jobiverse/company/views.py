from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from.models import Company,Job_Vacancy,Job_Application,Notification
from custom_admin.models import User
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationStatusForm
from django.core.paginator import Paginator
from django.db.models import Count
# from .signals import create_job_application_notification

# Create your views here.

@login_required
def home(request):
    page_number = request.GET.get('page',1)
    jobs = Job_Vacancy.objects.filter(company=request.user.company)
    company = Company.objects.get(user=request.user)

    applicants = Job_Application.objects.filter(job_vacancy__company=company)
    count = 0
    count = applicants.count()  
    # if applicants.status != 'submitted':
    #     count -= 1
    
       
    
    notification = 0
    notification = count
    
    paginator = Paginator(jobs,3)
    page = paginator.page(page_number)
    jobs = page.object_list
          
    context={
        'jobs':jobs,
        'company':company,
        'count':count,
        'applicants':applicants,
        'notifiaction':notification,
        'pages':list(range(1,paginator.num_pages+1))
    

    }
    return render(request,'company/home.html',context)


# notification on navbar <<------ -------->>

def notify_on_navbar(request):
    print('notify me')
    company = Company.objects.get(user=request.user)
    job_vacancies = Job_Vacancy.objects.filter(company=company)
    notify = Notification.objects.filter(job_vacancy__in=job_vacancies).order_by('-created_at')
    notification = 0
    
    for job_vacancy in job_vacancies:
        applicants = Job_Application.objects.filter(job_vacancy=job_vacancy)
        notification += applicants.count()
     
    context={
        "notification": notification,
        'notify':notify
    }
    print('notify me')
    return render(request,'company/notification.html',context)





def notification_count(request):
    
    company = Company.objects.get(user=request.user)
    applicants = Job_Application.objects.filter(job_vacancy__company=company)
    count = 0
    count = applicants.count()  
    
    context={
        'count':count
    }    
    
    return render(request,'company/base.html',context )



#notification end here  <<----- --------->




# company registeration
def company_register(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        logo = request.FILES.get('logo')
        decription = request.POST.get('description')
        password = request.POST.get('password')
        re_password = request.POST.get('password2')

        if password == re_password:
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_company=True
                )
                Company.objects.create(
                    user=user,
                    company_name=company_name,
                    email=email,
                    logo=logo,
                    website=website,
                    decription=decription,
                    status = "pending"
                )

                messages.success(request, 'Account created successfully')
                return redirect('signin')
            else:
                messages.error(request, 'Account already exists')
        else:
            messages.error(request, 'Invalid password or credentials')

    return render(request,'company/company_form.html')

#common-login
def sign_in(request):
    usr = None
    if request.user.is_authenticated:
        print(request.user.is_company)
        print(request.user.is_employee)
        print(request.user.is_admin)
        
        if request.user.is_company:
            return redirect('company_home')
        elif request.user.is_employee:
            return redirect('employee_home')
        else:
            return redirect('home_admin') 
                   
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            try:
                
                login(request, user)
                if user.is_company:
                    usr = Company.objects.get(user=user)
                    if  usr.status != "pending":
                        return redirect('company_home')
                    else:
                        messages.error(request, 'No account found')

                else: 
                    if user.is_employee:
                     
                        return redirect('employee_home')
                    else:
                        messages.error(request,'No Account Found')
                    
            except Company.DoesNotExist:
                raise Http404(' User Not Found or Not approved')
            except:
                messages.error(request, 'Invalid credentials')
    return render(request, 'company/signin.html', {'usr': usr})


def company_sign_out(request):
    logout(request)
    return redirect('signin')




#company-profile page
@login_required(login_url='signin')
def company_profile(request):
    if request.user.is_authenticated:
        try:
            company = Company.objects.get(user=request.user)

            context = {
            
                'company':company
            
            }

            return render(request,'company/profile.html',context)
    
        except Company.DoesNotExist:
            raise Http404('not available')

    else:
        raise Http404('you are not authorized to this page')       



# company- recruiting .
@login_required(login_url='signin')
def post_a_job(request):
    if request.method=='POST':
        designation = request.POST.get('designation')
        description = request.POST.get('description')
        location    = request.POST.get('location')

        job_vacancy = Job_Vacancy(designation=designation,
                        description=description,
                            location=location,
                            company=request.user.company,
                            )
        job_vacancy.save()
        return redirect('company_home')

    return render(request,'company/job_recruit.html')

@login_required(login_url='signin')
def applicant_list(request):
    applicants = Job_Application.objects.all()
      
    context={
       
        'applicants':applicants
    }
    return render(request,'company/applicants.html',context)

login_required(login_url='signin')
def posted_jobs(request):
    company = Company.objects.get(user=request.user)
    jobs = Job_Vacancy.objects.filter(company=company).annotate(applicant_count=Count('job_application'))
    
    
    job_counts = {}  # Dictionary to store job vacancy counts
    
    for job in jobs:
        applicants = Job_Application.objects.filter(job_vacancy=job)
        count = applicants.count()
        job_counts[job] = count
    
    context = {
        'jobs': jobs,
        'job_counts': job_counts,
    }
    
    return render(request, 'company/posted_jobs.html', context)

login_required(login_url='signin')
def profile_edit(request):
    company = request.user.company
    if request.method=='POST':
        company_name = request.POST.get('company_name')
        logo = request.FILES.get('logo')
        decription = request.POST.get('decription')
        website = request.POST.get('website')
        email = request.POST.get('email')
       
        company.company_name = company_name
        company.logo = logo
        company.decription = decription
        company.website = website
        company.email=email
        company.save()
        messages.success(request,'saved changes')

    context = {
        'company':company
    }
        
    return render(request,'company/company_editprofile.html',context)

login_required('signin')
def applicant_status(request,id):
    job_application = Job_Application.objects.get(id=id)
    if request.method == 'POST':
        form = JobApplicationStatusForm(request.POST, instance=job_application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job application status has been updated.')
            return redirect('applicants_list') 
    else:
        form = JobApplicationStatusForm(instance=job_application)
    return render(request,'company/applicant_status.html',{'form': form})

login_required(login_url='signin')
def edit_post(request):
    jobs= Job_Vacancy.objects.filter(company = request.user.company)
    return render(request,"company/post.html",{'jobs':jobs})

login_required(login_url='signin')
def edit_job_post(request,id):
    job_vacancy = Job_Vacancy.objects.get(id = id)
    if request.method =='POST':
        designation = request.POST.get('designation')
        description = request.POST.get('description')
        location    = request.POST.get('location')

        job_vacancy.designation = designation
        job_vacancy.description = description
        job_vacancy.location = location
        job_vacancy.save()
        messages.success(request,'saved changes')
        return redirect('edit_post')


    return render(request,'company/edit_job_post.html',{'job_vacancy':job_vacancy })







