from django.urls import path,include
from . import views
from.views import PasswordsChangeView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('success/', views.succesmessage, name='success_message'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html'), name='change_password'),

     
     
     path('password_reset/done/', 
     auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_dn.html'), 
     name='password_reset_done'),
   
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), 
    name='password_reset_confirm'),
    
     path('password_reset/', 
     auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), 
     name='password_reset'),
    
    path('reset/done/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),      
 
]
