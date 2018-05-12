from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse

from website.models.home_tab import HomeTab
from website.models.post import Post
from website.views import salon as salon_views
from website.views.base import get_login_modal


def get_header(request):
    current_tab = request.GET.get('tab', None)

    nav_items = []
    nav_items.append({
        'name': '全部活動',
        'link': reverse('home'),
        'current': current_tab is None
    })
    for tab in HomeTab.objects.order_by('order').all():
        nav_items.append({
            'name': tab.name,
            'link': '%s?tab=%s' % (reverse('home'), tab.name),
            'current': current_tab == tab.name
        })
    return {
        'nav_items': nav_items,
        'modal': get_login_modal(request)
    }


def home(request):
    tab = request.GET.get('tab', None)
    if tab:
        posts = Post.objects.filter(tags__name__in=[tab])
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
