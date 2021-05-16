from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='authentication:login')
def home_view(request):
    return render(request,'mainapp/home.html',{})