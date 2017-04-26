"""PartyBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from Bot import views as bot_views

urlpatterns = [
    url(r'^$', bot_views.week, name='week'),
    url(r'^day/(?P<num>[0-9]+)$', bot_views.day, name='day'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},  name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', bot_views.signup, name='signup'),
    url(r'^add_event/(?P<num>[0-9]+)$', bot_views.add_event, name='add_event'),
    url(r'^edit_event/(?P<id>[0-9]+)/(?P<num>[0-9]+)$', bot_views.edit_event, name='edit_event'),
    url(r'^delete_event/(?P<id>[0-9]+)/(?P<num>[0-9]+)$', bot_views.delete_event, name='delete_event'),
    url(r'^list_user/$', bot_views.list_user, name='list_user'),
    url(r'^list_action/$', bot_views.list_action, name='list_action'),
    url(r'^change_vip/(?P<user_telegram_id>[0-9]+)$', bot_views.change_vip, name='change_vip'),
    url(r'^delete_all_event/(?P<num>[0-9]+)$', bot_views.delete_all_event, name='delete_all_event'),
    url(r'^list_advertisement/$', bot_views.list_advertisement, name='list_advertisement'),
    url(r'^add_advertisement/$', bot_views.add_advertisement, name='add_advertisement'),
    url(r'^edit_advertisement/(?P<id>[0-9]+)$', bot_views.edit_advertisement, name='edit_advertisement'),
    url(r'^delete_advertisement/(?P<id>[0-9]+)$', bot_views.delete_advertisement, name='delete_advertisement'),
]

import Bot.bot # bot's initialization