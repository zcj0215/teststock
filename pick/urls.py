
from django.urls import re_path,path
from .import views as pick_views

urlpatterns = [ 
    re_path(r'^$', pick_views.home, name='home'),
    path('query/', pick_views.query,name='query'),  
    path('jquery/', pick_views.jquery,name='jquery'),  
]