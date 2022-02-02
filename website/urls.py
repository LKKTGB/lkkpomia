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
from django.urls import include, path, reverse
from django.views.generic.base import RedirectView

from website import views as website_views
from website.views import policy as policy_views
from website.views import posts as posts_views
from website.views import salon as salon_views
from website.views import video_contest as video_contest_views


class HomeRedirectView(RedirectView):

    permanent = False
    pattern_name = 'posts/1'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('post', kwargs={'post_id': 1})


urlpatterns = [
    # path('', HomeRedirectView.as_view(), name='home'),
    path('', posts_views.Posts.as_view(show_headline=True), name='home'),
    path('policies/privacy', policy_views.privacy, name='policy_privacy'),
    path('posts/', posts_views.Posts.as_view(show_headline=False), name='posts'),
    path('posts/<post_id>/', website_views.post, name='post'),
    path('posts/<post_id>/form', website_views.form, name='form'),
    path('posts/<post_id>/forms/', salon_views.SalonForms.as_view(), name='forms'),
    path('posts/<post_id>/forms/<form_id>', salon_views.delete_form, name='form_delete'),
    path('posts/<post_id>/thanks', website_views.thanks, name='thanks'),
    path('posts/<post_id>/gallery', video_contest_views.Gallery.as_view(), name='gallery'),
    path('posts/<post_id>/winners', video_contest_views.Winners.as_view(), name='winners'),
    path('posts/<post_id>/videos/<video_number>', video_contest_views.Video.as_view(), name='video'),
    path('posts/<post_id>/videos/<video_number>/votes',
         video_contest_views.vote, name='video_votes'),
    path('video_contests/<video_contest_id>/info/',
         video_contest_views.info, name='video_contest_info'),
    path('video_contests/<video_contest_id>/announcements/',
         video_contest_views.announcements, name='video_contest_announcements'),
    path('video_contests/<video_contest_id>/winners/',
         video_contest_views.winners, name='video_contest_winners'),
    path('video_contests/<video_contest_id>/gallery/',
         video_contest_views.gallery, name='video_contest_gallery'),
    path('video_contests/<video_contest_id>/videos/<video_number>',
         video_contest_views.video, name='video_contest_video'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('social_django.urls', namespace='social')),
    path('grappelli/', include('grappelli.urls')),
    path("tinymce/", include("tinymce.urls")),
]
