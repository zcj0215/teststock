
from django.urls import path, re_path
from . import views

urlpatterns = [ 
   re_path(r'^$', views.redirect_root,name='home'),        
   path('pred', views.pred, name='pred'),
   path('pypred', views.pypred, name='pypred'),
]