from authentication.forms import RegisterForm
from django.shortcuts import redirect, render
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('mainapp:home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account succefully created!!")
            return redirect('mainapp:home')
    return render(request,'authentication/auth_register.html',{"form":form})

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
    return render(request,'authentication/auth_login.html',{})

def logout_view(request):
    logout(request)
    return redirect('authentication:login')