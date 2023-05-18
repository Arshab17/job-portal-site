from django.db import models
from custom_admin.models import User
from employee_account.models import Employee
# Create your models here.


class Company(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200,unique=True)
    email = models.CharField(max_length=250,unique=True)
    logo = models.ImageField(blank=True,null=True,upload_to='logos/')
    website = models.CharField(max_length=250,null=True,blank=True)
    decription = models.TextField(max_length=500,null=True,blank=True)
    status  = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.company_name
        

class Job_Vacancy(models.Model):
    company     = models.ForeignKey(Company,on_delete=models.CASCADE)
    designation = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    location    = models.CharField(max_length=20,blank=True,null=True)
    applicants  = models.ManyToManyField(Employee,related_name='job_applied')
    posted      = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.designation
    


class Job_Application(models.Model):
    APPLICATION_STATUS_CHOICES = (
    ('submitted', 'Submitted'),
    ('reviewed', 'Reviewed'),
    ('shortlisted', 'Shortlisted'),
    ('rejected', 'Rejected'),
   
)
    employee    = models.ForeignKey(Employee,on_delete=models.CASCADE)
    job_vacancy = models.ForeignKey(Job_Vacancy,on_delete=models.CASCADE)
    resume      = models.FileField(upload_to='resumes/')
    cover_letter= models.CharField(max_length=500)
    applied     = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(max_length=20,choices=APPLICATION_STATUS_CHOICES,default='submitted')     

    def __str__(self):
        return f"{self.employee.user.first_name} - {self.job_vacancy.designation}"
    

class Notification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job_vacancy = models.ForeignKey(Job_Vacancy, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
