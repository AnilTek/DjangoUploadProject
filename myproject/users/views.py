from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm  
from django.contrib.auth.backends import ModelBackend

# Create your views here.
from .forms import CustomUserCreationForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Username olarak email kullanılıyor
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('upload:entry')  # Ana sayfaya yönlendirme
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user(), backend='django.contrib.auth.backends.ModelBackend')
            return redirect('upload:entry')  # Ana sayfaya yönlendirme
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {"form": form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')

    
def anil(request):
    return render(request,"users/anil.html")
