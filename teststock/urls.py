"""teststock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,re_path,include
from django.contrib.auth import views as auth_views
from boards import views as boards_views
from accounts import views as accounts_views
from astocks import views as astocks_views


urlpatterns = [
    re_path(r'^$', boards_views.redirect_root, name='home'),
    re_path(r'^signup/$', accounts_views.signup, name='signup'),
    re_path(r'^login/$', accounts_views.login, name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
    re_path(r'^api/(?P<code>\d+)$', astocks_views.single),
    re_path(r'^api/stockSql/$',astocks_views.stockList),
    re_path(r'^api/search/$',astocks_views.search),
    re_path(r'^api/query/$',astocks_views.query),
    re_path(r'^person/$', accounts_views.new_person,name='new_person'),
    re_path(r'^pick/$', accounts_views.new_pick,name='new_pick'),
    re_path(r'^handledd/$', astocks_views.handledd,name='handledd'),
    re_path(r'^handleto/$', astocks_views.handleto,name='handleto'),
    path('admin/', admin.site.urls),
    path('boards/', include(('boards.urls','boards'),namespace='boards')),
    path('prediction/', include(('prediction.urls','prediction'),namespace='prediction')),
]
