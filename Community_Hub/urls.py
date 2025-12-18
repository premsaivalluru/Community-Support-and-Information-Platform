from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('register/', views.register, name='Register Page'),
    path('login/', views.login, name='Login Page'),
    path('all_posts/', views.all_posts, name='All Posts Page'),
    path('create_post/', views.create_post, name='Create Post Page'),
    path('about/', views.about, name='About Page'),
    path('feedback/', views.feedback, name='Feedback Page'),
    path('contact/', views.contact, name='Contact Page'),
    path('profile/<str:username>/', views.profile, name = 'Profile Page'),
    path('register_phone_verify/', views.register_phone_verify, name='Register Phone Verify'),
    path('register_phone_verify_otp/', views.register_phone_verify_otp, name="Register Phone Verify OTP"),
    path('register/get_started/', views.get_started_form, name = "Submit Get Started Form"),
    path('logout/', views.logout_page, name="Logout Page"),
    path('login_user/', views.login_user, name="Login User"),
    path('login_phone_verify/', views.login_phone_verify, name='Login Phone Verify'),
    path('login_phone_verify_otp/', views.login_phone_verify_otp, name="Login Phone Verify OTP"),
    path('reset_password/', views.reset_password, name="Reset Password"),
    path('create_post_submit/', views.create_post_submit, name="Create Post"),
    #path('sms_reply', views.sms_reply, name="SMS Reply"),
    path('submit_feedback/', views.submit_feedback, name="Submit Feedback"),
    path('submit_contact/', views.submit_contact, name="Submit Contact"),
    path('submit_filter_request/', views.submit_filter_request, name="Submit Filter Request"),
]
