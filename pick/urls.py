
from django.urls import re_path,path
from . import views as pick_views
from .view import pick_views as select_views

urlpatterns = [ 
    re_path(r'^$', pick_views.home, name='home'),
    path('query/', pick_views.query,name='query'),  
    path('jquery/', pick_views.jquery,name='jquery'), 
    path('dayadd/', pick_views.dayadd,name='dayadd'), 
    path('blockadd/', pick_views.blockadd,name='blockadd'), 
    path('indexadd/', pick_views.indexadd,name='indexadd'), 
    path('blockdayadd/', pick_views.blockdayadd,name='blockdayadd'), 
    path('dayout/', pick_views.dayout,name='dayout'), 
    path('inflow/', pick_views.inflow,name='inflow'),
    path('inflow_single/', pick_views.inflow_single,name='inflow_single'),
    path('inflow_files/', pick_views.inflow_files,name='inflow_files'),
    path('stock_single/', pick_views.stock_single,name='stock_single'),
    path('stock_select/', select_views.stock_select,name='stock_select'),
    path('index_single/', pick_views.index_single,name='index_single'),
]
