from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('tag/<str:tag>/',views.home_view,name='tag'),
    path('error/',views.error,name='error'),
    path('linksave/',views.link_save,name='linksave'),    
    path('click/<str:urlslug>',views.link_click,name='click'),
    path('approval/<str:urlslug>',views.approvalView,name='approval'),
]

