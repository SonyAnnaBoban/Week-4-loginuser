from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginn, name='login'),
    path('signup/', views.signuppage, name='signup'),
    path('homepage/',views.home,name='homepage'),
    path('logout/',views.logout,name='logout'),
    path('contact/',views.contact,name='contact'),
    
]
