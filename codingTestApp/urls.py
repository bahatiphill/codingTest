from django.urls import path
from .views import home, upload_users_file, users_list, commit_to_db, savedUsers

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_users_file, name='upload'),
    path('commit/', commit_to_db, name='commit'),
    path('validatedusers/', users_list, name='validatedusers'),
    path('savedusers/', savedUsers, name='savedusers')
    
]