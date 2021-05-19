from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('linksave/',views.link_save,name='linksave'),    
    path('taglinks/',views.related_tags,name='taglinksnocontext'),
    path('taglinks/<str:tag>/',views.related_tags,name='taglinks'),
]
