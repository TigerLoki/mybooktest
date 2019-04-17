from django.shortcuts import redirect
from django.urls import path, re_path, include
from mybook import views

urlpatterns = [
    re_path(r'^books/', views.get_books),
    path('', views.login),
]
