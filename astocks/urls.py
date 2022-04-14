
from django.urls import re_path
from .view import pick_views

urlpatterns = [ 
    re_path(r'^$', pick_views.StockChooseListView.as_view(), name='home'),
    re_path(r'^edit_pick/(?P<id>\d+)/$', pick_views.EditStockChooseView.as_view(), name='edit_pick'), 
    re_path(r'^delete_pick/(?P<id>\d+)/$', pick_views.DeleteStockChooseView.as_view(), name='delete_pick'), 
    re_path(r'^edit_pick/(?P<id>\d+)/(?P<by>[a-z]+)/$', pick_views.EditStockChooseView.as_view(), name='edit_pick_by_date'), 
    re_path(r'^delete_pick/(?P<id>\d+)/(?P<by>[a-z]+)/$', pick_views.DeleteStockChooseByDateView.as_view(), name='delete_pick_by_date'), 
    re_path(r'^choose_date/$', pick_views.byDateListView,name='choose_date'),  
]