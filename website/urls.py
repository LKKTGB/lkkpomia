"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import include, path

from website import views as website_views
from website.views import video_contest as video_contest_views

urlpatterns = [
    path('', website_views.profile, name='home'),
    path('video_contests/<video_contest_id>/info/',
         video_contest_views.info, name='video_contest_info'),
    path('video_contests/<video_contest_id>/announcements/',
         video_contest_views.announcements, name='video_contest_announcements'),
    path('video_contests/<video_contest_id>/form/',
         video_contest_views.form, name='video_contest_form'),
    path('video_contests/<video_contest_id>/winners/',
         video_contest_views.winners, name='video_contest_winners'),
    path('video_contests/<video_contest_id>/gallery/',
         video_contest_views.gallery, name='video_contest_gallery'),
    path('video_contests/<video_contest_id>/videos/<video_id>',
         video_contest_views.video, name='video_contest_video'),
    path('video_contests/<video_contest_id>/thanks/',
         video_contest_views.thanks, name='video_contest_thanks'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('', include('social_django.urls', namespace='social')),
    path('grappelli/', include('grappelli.urls')),
]
