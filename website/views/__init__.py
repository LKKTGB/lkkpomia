from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse

from website import models
from website.views.event import Event
from website.views.form import SalonRegistrationFormView
from website.views.salon import Salon

from website.views.base import get_login_modal


def post(request, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect('home')
    if hasattr(post, 'event'):
        if hasattr(post.event, 'videocontest'):
            return redirect('video_contest_info', video_contest_id=post.id)
        elif hasattr(post.event, 'salon'):
            return Salon.as_view()(request, pk=post_id)
    return redirect('home')


def form(request, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect('home')
    if hasattr(post, 'event'):
        if hasattr(post.event, 'salon'):
            return SalonRegistrationFormView.as_view()(request, pk=post_id)
    return redirect('home')


def thanks(request, post_id):
    return render(request, 'thanks.html', {
        'post_id': post_id,
        'countdown': 10
    })
