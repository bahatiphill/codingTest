from django.contrib import admin
from django.urls import path, include
from .views import home, upload_users_file, users_list, commit_to_db

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_users_file, name='upload'),
    path('commit/', commit_to_db, name='commit'),
    path('users/', users_list, name='users'),
    
]