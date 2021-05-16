from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LinkForm
from .models import Link

# Create your views here.
@login_required(login_url='authentication:login')
def home_view(request):
    form = LinkForm()
    links = Link.objects.all().order_by('-date')
    return render(request,'mainapp/home.html',{"form":form,"links":links})

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
