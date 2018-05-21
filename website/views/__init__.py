from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from website import models
from website.views.salon import Salon, SalonRegistrationFormView
from website.views.video_contest import Thanks, VideoContest, VideoContestRegistrationFormView


def post(request, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect('home')
    if hasattr(post, 'event'):
        if hasattr(post.event, 'videocontest'):
            return VideoContest.as_view()(request, pk=post_id)
        elif hasattr(post.event, 'salon'):
            return Salon.as_view()(request, pk=post_id)
    return redirect('home')


def form(request, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect('home')
    if hasattr(post, 'event'):
        if hasattr(post.event, 'videocontest'):
            return VideoContestRegistrationFormView.as_view()(request, pk=post_id)
        elif hasattr(post.event, 'salon'):
            return SalonRegistrationFormView.as_view()(request, pk=post_id)
    return redirect('home')


def thanks(request, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect('home')

    if not hasattr(post, 'event'):
        return redirect('post', post_id=post_id)

    if hasattr(post.event, 'videocontest'):
        return Thanks.as_view()(request, pk=post_id)
    else:
        return render(request, 'thanks.html', {
            'post_id': post_id,
            'countdown': 10
        })
