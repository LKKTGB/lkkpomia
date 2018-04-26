from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse

from website.models.post import Post
from website.views.base import get_login_modal


def get_header(request):
    current_tag = request.GET.get('tag', None)

    nav_items = []
    nav_items.append({
        'name': '全部活動',
        'link': reverse('home'),
        'current': current_tag is None
    })
    for tag_name in ['有影講台語', '台語sa攏有']:
        nav_items.append({
            'name': tag_name,
            'link': '%s?tag=%s' % (reverse('home'), tag_name),
            'current': current_tag == tag_name
        })
    return {
        'nav_items': nav_items,
        'modal': get_login_modal(request)
    }


def home(request):
    tag = request.GET.get('tag', None)
    if tag:
        posts = Post.objects.filter(tags__name__in=[tag])
    else:
        posts = Post.objects.all()

    return render(request, 'posts.html', {
        'meta_title': '李江却台語文教基金會',
        'home': False,
        'user': request.user,
        'posts': posts,
        'header': get_header(request)
    })


def post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect('home')
    if hasattr(post, 'event'):
        if hasattr(post.event, 'videocontest'):
            return redirect('video_contest_info', video_contest_id=post.id)
    return redirect('home')
