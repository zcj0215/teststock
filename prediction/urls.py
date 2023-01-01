
from django.urls import path, re_path
from . import views

urlpatterns = [ 
   re_path(r'^$', views.redirect_root,name='home'),        
   path('pred', views.pred, name='pred'),
   path('search', views.search, name='predict_stock'),
   path("home2",views.home2,name='home2'),
   path("predict",views.predict_stock_action,name='predict'),
]