from mainapp import urls
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import LinkForm
from .models import Click, Link
from django.core.paginator import Paginator
from django.db.models import F
import random, string
from django.contrib import messages

# Create your views here.

def error(request,exception):
    return render(request,'error.html',{})

@login_required(login_url='account_login')
def home_view(request,tag=""):
    click = Click.objects.filter(Q(userref=request.user) & Q(status=False)).first()
    if click is not None:
        return redirect('mainapp:approval',urlslug=click.linkref.urlslug)
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
                link_list = Link.objects.all().order_by('-likes')
    paginator = Paginator(link_list, 10) 
    page_number = request.GET.get('page')
    links = paginator.get_page(page_number)
    return render(request,'mainapp/home.html',{"form":form,"links":links,"search":keyword or ""})

@login_required(login_url='account_login')
def related_tags(request,tag=""):
    form = LinkForm()
    links = []
    if request.method == 'GET':
        link_list = Link.objects.filter(tags__name=tag).order_by('-date')
        paginator = Paginator(link_list, 10) 
        page_number = request.GET.get('page')
        links = paginator.get_page(page_number)
    return render(request,'mainapp/relatedlinks.html',{"links":links,"form":form})

@login_required(login_url='account_login')
def approvalView(request,urlslug):
    link = Link.objects.get(urlslug=urlslug)
    if not Click.objects.filter( Q(linkref=link) & Q(userref=request.user) ).exists():
        messages.warning(request,"Can't approve without using the link!!")
        return redirect('mainapp:home')
    if request.method == 'POST':
        print(request.POST)
        op = request.POST.get('approved',0)
        if op == 0:
            print("disliked")
            Link.objects.filter(urlslug=urlslug).update(dislikes=F('dislikes')+1)
        else:
            Link.objects.filter(urlslug=urlslug).update(likes=F('likes')+1)
        Click.objects.filter( Q(linkref=link) & Q(userref=request.user) ).update(status=True)
        return redirect('mainapp:home')
    return render(request,'mainapp/approval.html',{"link":link})

@login_required(login_url='account_login')
def link_click(request,urlslug):
    l = Link.objects.get(urlslug=urlslug)
    obj,created = Click.objects.get_or_create(linkref=l,userref=request.user,defaults={'status':False})
    if created is True:
        l.clicks += 1
        l.save()
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
