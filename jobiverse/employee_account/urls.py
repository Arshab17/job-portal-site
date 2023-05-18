from django.urls import path
from .views import*


urlpatterns = [
    path('register/',register,name='register'),
    # path('signin',sign_in,name='signin'),
    path('signout',sign_out,name='signout'),
    path('home',home,name='employee_home'),
    path('profile/',employee_profile,name="employee_profile"),
    path('job_application/<int:id>/create/', job_application_create, name='job_application_create'),
    path('job_application',job_application_detail, name='job_application_detail'),
    path('edit/profile/',employee_profile_edit,name="emp_edit"),
    path('notification/',my_jobs,name='jobs_notification')
    



]