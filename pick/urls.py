
from django.urls import re_path,path
from .import views as pick_views

urlpatterns = [ 
    re_path(r'^$', pick_views.home, name='home'),
    path('query/', pick_views.query,name='query'),  
    path('jquery/', pick_views.jquery,name='jquery'), 
    path('dayadd/', pick_views.dayadd,name='dayadd'), 
    path('blockadd/', pick_views.blockadd,name='blockadd'), 
    path('blockdayadd/', pick_views.blockdayadd,name='blockdayadd'), 
    path('dayout/', pick_views.dayout,name='dayout'), 
    path('inflow/', pick_views.inflow,name='inflow'),
    path('inflow_single/', pick_views.inflow_single,name='inflow_single'),
    path('stock_single/', pick_views.stock_single,name='stock_single'),
]
