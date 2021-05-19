from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LinkForm
from .models import Link
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='authentication:login')
def home_view(request):
    form = LinkForm()
    link_list=[]
    if request.method == 'GET':
        keyword = request.GET.get('search')
        if keyword is not None and keyword is not "":
            link_list = Link.objects.filter(title__startswith=keyword).order_by('-date')[:10]
        else:    
            link_list = Link.objects.all()
    paginator = Paginator(link_list, 5) 
    page_number = request.GET.get('page')
    links = paginator.get_page(page_number)
    return render(request,'mainapp/home.html',{"form":form,"links":links,"search":keyword or ""})

# def search_view(request):
#     form = LinkForm()
#     links = []
#     if request.method == 'GET':
#         keyword = request.GET.get('search')
#         if keyword is not None and keyword is not "":
#             link_list = Link.objects.filter(title__startswith=keyword).order_by('-date')[:10]
#             paginator = Paginator(link_list, 5) 
#             page_number = request.GET.get('page')
#             links = paginator.get_page(page_number)
#             print(keyword,page_number)
#     return render(request,'mainapp/home.html',{"links":links,"form":form,"search":keyword or ""})

def related_tags(request,tag=""):
    form = LinkForm()
    links = []
    if request.method == 'GET':
        links = Link.objects.filter(tags__name=tag).order_by('-date')[:10]
    return render(request,'mainapp/relatedlinks.html',{"links":links,"form":form})

def link_save(request):
    if request.is_ajax and request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid:
            f = form.save(commit=False)
            f.uploaded_by = request.user
            f.save()
            form.save_m2m()
            return JsonResponse({"message":"success"},status=200)
        else:
            return JsonResponse({"message":form.errors},status=400)
    return JsonResponse({"message":"unknown error"},status=200)
