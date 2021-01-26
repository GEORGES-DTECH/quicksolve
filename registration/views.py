from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView



class PasswordsChangeView(PasswordChangeView):
    success_url = reverse_lazy('success_message')
    from_class = PasswordChangeForm

def succesmessage(request):
    return render(request,'registration/success.html')




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created,you can login')
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
