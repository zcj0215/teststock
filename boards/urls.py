
from django.urls import path, re_path
from . import views

urlpatterns = [ 
    re_path(r'^$', views.BoardListView.as_view(), name='home'),  
    re_path(r'^(?P<pk>\d+)/types/(?P<type_pk>\d+)/$', views.ByTypeBoardListView.as_view(), name='type_boards'), 
    re_path(r'^(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    re_path(r'^(?P<name>.+)/stocks/$', views.StockListView.as_view(), name='board_stocks'),
    re_path(r'^(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    re_path(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    re_path(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    re_path(r'^(?P<board_name>.+)/stocks/(?P<stock_name>.+)/$', views.stock_detail, name='stock_detail'),
    re_path(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/edit/$',
        views.TopicUpdateView.as_view(), name='edit_topic'),  
    re_path(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),  
    path('query', views.query, name='query'),
    path('blockquery', views.blockquery, name='blockquery'),  
    path('blockget', views.blockget, name='blockget'),  
]