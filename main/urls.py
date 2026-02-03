from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
