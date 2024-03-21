from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

def login(request):
    context = {'page_title': 'Login'}
    return render(request, 'authentication/login.html', context=context)

def register(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        # form = UserCreationForm()
        form = UserRegisterForm()
    context = {'page_title': 'Register', 'form': form}
    return render(request, 'authentication/register.html', context=context)