from django.db.models.expressions import Case, ExpressionWrapper, When
from django.db.models.fields import BooleanField
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import LinkForm
from .models import Link
from django.core.paginator import Paginator
from django.db.models import F
import random, string
from django.contrib import messages
from django.core import serializers

# Create your views here.

def error(request,exception):
    return render(request,'error.html',{})

def home_view(request,tag=""):
    form = LinkForm()
    link_list=[]
    if tag != "":
        link_list = Link.objects.filter(tags__name=tag).order_by('-date')
        keyword=""
    else:
        if request.method == 'GET':
            keyword = request.GET.get('search')
            if keyword is not None and keyword != "":
                link_list = Link.objects.filter(Q(title__startswith=keyword)|Q(title__icontains=keyword)|Q(tags__name=keyword)).distinct().order_by('-date')
            else:
                link_list = Link.objects.all().order_by('-date')
    paginator = Paginator(link_list, 10) 
    page_number = request.GET.get('page')
    links = paginator.get_page(page_number)
    return render(request,'mainapp/home.html',{"form":form,"links":links,"search":keyword or "","tag":tag})

def report(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login first to report the link!!")
        return JsonResponse({"message":"loginrequired"},status=200)
    if request.is_ajax and request.method == 'POST':
        urlslug = request.POST.get('urlslug')
        link = Link.objects.get(urlslug=urlslug)
        c=link.reported_by.add(request.user)
        print(c)
        return JsonResponse({"message":"reported"},status=200)

@login_required(login_url='account_login')
def link_click(request,urlslug):
    l = Link.objects.get(urlslug=urlslug)
    Link.objects.filter(urlslug=urlslug).update(clicks=F('clicks')+1)
    return redirect(l.link)

#utility function
def shortit(url):
    N = 7
    s = string.ascii_uppercase + string.ascii_lowercase + string.digits
    url_id = ''.join(random.choices(s, k=N))
    if not Link.objects.filter(urlslug=url_id).exists():
        return url_id
    else:
        shortit(url)

@login_required(login_url='account_login')
def link_save(request):
    if request.is_ajax and request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid:
            f = form.save(commit=False)
            slug = shortit(form.cleaned_data['link'])
            f.urlslug = slug
            f.uploaded_by = request.user
            f.save()
            form.save_m2m()
            return JsonResponse({"message":"success"},status=200)
        else:
            return JsonResponse({"message":form.errors},status=400)
    return JsonResponse({"message":"unknown error"},status=200)
