from django.urls import path
from . import views
from.views import PasswordsChangeView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('success/', views.succesmessage, name='success_message'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html'), name='change_password'),
]
