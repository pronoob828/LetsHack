from django.urls import path
from accounts.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path("resend_email",resend_email,name="resend_email"),
     path("register/",registration_view,name="register"),
    path("logout/",logout_view,name="logout"),
    path("login/",login_view,name="login"),
    
    # Email verification
    path('email/<str:token>/',confirm), 

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth_registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='auth_registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "auth_registration/password_reset_confirm.html"),
    name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth_registration/password_reset_form.html', 
    email_template_name ="auth_registration/password_reset_email.html"), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_registration/password_reset_complete.html'),
     name='password_reset_complete'),

]