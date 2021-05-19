from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('tag/<str:tag>/',views.home_view,name='tag'),
    path('linksave/',views.link_save,name='linksave'),    
    path('click/<int:id>',views.link_click,name='click'),
    path('approval/<int:id>',views.approvalView,name='approval'),
]
