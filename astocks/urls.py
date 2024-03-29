
from django.urls import re_path
from .view import pick_views,limitup_views

urlpatterns = [ 
    re_path(r'^$', pick_views.StockChooseListView.as_view(), name='home'),
    re_path(r'^edit_pick/(?P<id>\d+)/$', pick_views.EditStockChooseView.as_view(), name='edit_pick'), 
    re_path(r'^delete_pick/(?P<id>\d+)/$', pick_views.DeleteStockChooseView.as_view(), name='delete_pick'), 
    re_path(r'^edit_pick/(?P<id>\d+)/(?P<by>[a-z]+)/$', pick_views.EditStockChooseView.as_view(), name='edit_pick_by_date'), 
    re_path(r'^delete_pick/(?P<id>\d+)/(?P<by>[a-z]+)/$', pick_views.DeleteStockChooseByDateView.as_view(), name='delete_pick_by_date'), 
    re_path(r'^edit_pick/(?P<id>\d+)/(?P<bytype>\d+)/$', pick_views.EditStockChooseView.as_view(), name='edit_pick_by_type'), 
    re_path(r'^delete_pick/(?P<id>\d+)/(?P<bytype>\d+)/$', pick_views.DeleteStockChooseByTypeView.as_view(), name='delete_pick_by_type'), 
    re_path(r'^edit_pick/(?P<id>\d+)/(?P<byboard>\d+)/$', pick_views.EditStockChooseView.as_view(), name='edit_pick_by_board'), 
    re_path(r'^delete_pick/(?P<id>\d+)/(?P<byboard>\d+)/$', pick_views.DeleteStockChooseByBoardView.as_view(), name='delete_pick_by_board'), 
    re_path(r'^choose_date/$', pick_views.byDateListView,name='choose_date'),  
    re_path(r'^choose_type/$', pick_views.byTypeListView,name='choose_type'), 
    re_path(r'^choose_board/$', pick_views.byBoardListView,name='choose_board'),   
    re_path(r'^choose_detail/(?P<name>.+)/$', pick_views.choose_detail,name='choose_detail'), 
    re_path(r'^limitup/$', limitup_views.StockChooseListView.as_view(), name='limitup'),
    re_path(r'^edit_limitup/(?P<id>\d+)/$', limitup_views.EditStockChooseView.as_view(), name='edit_limitup'), 
    re_path(r'^delete_limitup/(?P<id>\d+)/$', limitup_views.DeleteStockChooseView.as_view(), name='delete_limitup'), 
    re_path(r'^edit_limitup/(?P<id>\d+)/(?P<by>[a-z]+)/$', limitup_views.EditStockChooseView.as_view(), name='edit_limitup_by_date'), 
    re_path(r'^delete_limitup/(?P<id>\d+)/(?P<by>[a-z]+)/$', limitup_views.DeleteStockChooseByDateView.as_view(), name='delete_limitup_by_date'), 
    re_path(r'^edit_limitup/(?P<id>\d+)/(?P<bytype>\d+)/$', limitup_views.EditStockChooseView.as_view(), name='edit_limitup_by_type'), 
    re_path(r'^delete_limitup/(?P<id>\d+)/(?P<bytype>\d+)/$', limitup_views.DeleteStockChooseByTypeView.as_view(), name='delete_limitup_by_type'), 
    re_path(r'^edit_limitup/(?P<id>\d+)/(?P<byboard>\d+)/$', limitup_views.EditStockChooseView.as_view(), name='edit_limitup_by_board'), 
    re_path(r'^delete_limitup/(?P<id>\d+)/(?P<byboard>\d+)/$', limitup_views.DeleteStockChooseByBoardView.as_view(), name='delete_limitup_by_board'), 
    re_path(r'^limitup_date/$', limitup_views.byDateListView,name='limitup_date'),
    re_path(r'^limitup_type/$', limitup_views.byTypeListView,name='limitup_type'),
    re_path(r'^limitup_board/$', limitup_views.byBoardListView,name='limitup_board'),
    re_path(r'^limitup_detail/(?P<name>.+)/$', limitup_views.limitup_detail,name='limitup_detail'), 
]