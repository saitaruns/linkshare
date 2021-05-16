from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('mainapp:home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account succefully created!!")
            return redirect('mainapp:home')
        else:
            messages.error(request,"Error while creating the account")
    form = UserCreationForm()
    return render(request,'authentication/register.html',{"form":form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('mainapp:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in!!")
            return redirect('mainapp:home')
        else:
            messages.error(request,"Incorrect Information")
    return render(request,'authentication/login.html',{})

def logout_view(request):
    logout(request)
    return redirect('login')