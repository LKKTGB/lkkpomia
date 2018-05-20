from collections import OrderedDict
from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.template.defaultfilters import date
from django.urls import reverse
from django.utils import timezone

from website import models
from website.forms import VideoContestRegistrationForm, VideoContestVoteForm
from website.utils import handle_old_connections
from website.views.base import get_login_modal
from website.views.event import Event

from django.urls import resolve


def get_nav_items(video_contest, request):
    now = timezone.now()
    contest_started = now > video_contest.registration_start_time

    current_tab = resolve(request.path_info).url_name

    nav_items = []
    nav_items.append({
        'name': '活動內容',
        'link': reverse('post', kwargs={'post_id': video_contest.id}),
        'current': current_tab == 'post'
    })
    if contest_started:
        nav_items.append({
            'name': '參賽影片',
            'link': reverse('video_contest_gallery', kwargs={'video_contest_id': video_contest.id}),
            'current': current_tab == 'gallery'
        })
    return nav_items


def get_sidebar_info(video_contest):
    info = OrderedDict()
    info['calendar'] = ['%s ~ %s' % (date(video_contest.start_time, 'Y/m/d'), date(video_contest.end_time, 'Y/m/d'))]
    info['people'] = ['已有 %d 人報名成功' % models.VideoContestRegistration.objects.filter(
        event=video_contest, qualified=True).count()]
    return info


class VideoContest(Event):
    template_name = 'event.html'
    model = models.VideoContest

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['nav_items'] = get_nav_items(self.object, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.object)
        context_data['registration_modal'] = self.get_registration_modal()
        return context_data


def info(request, video_contest_id):
    return redirect('post', post_id=video_contest_id)


def get_header(request, video_contest, current):
    now = timezone.now()
    headers = {}
    headers['活動內容'] = 'info'
    # headers['最新公告']= 'announcements'
    if now > video_contest.registration_start_time:
        headers['參賽影片'] = 'gallery'
        if models.VideoContestWinner.objects.filter(video_contest=video_contest).exists():
            headers['得獎影片'] = 'winners'

    items = []
    for name, view in headers.items():
        items.append({
            'name': name,
            'link': reverse('video_contest_%s' % view, kwargs={'video_contest_id': video_contest.id}),
            'current': view == current
        })
    return {
        'nav_items': items,
        'modal': get_login_modal(request)
    }


@handle_old_connections
def announcements(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


@login_required
@handle_old_connections
def form_post(request, video_contest_id):
    try:
        video_contest = models.VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    form = VideoContestRegistrationForm(data=request.POST, video_contest=video_contest)
    if form.is_valid():
        registration = models.VideoContestRegistration(
            submitter=request.user,
            event=video_contest,
            contestant_name=form.cleaned_data['contestant_name'],
            phone_number=form.cleaned_data['phone_number'],
            address=form.cleaned_data['address'],
            email=form.cleaned_data['email'],
            video_title=form.cleaned_data['video_title'],
            introduction=form.cleaned_data['introduction'],
            youtube_url=form.cleaned_data['youtube_url'],
            group=form.cleaned_data['group'],
            questions=form.cleaned_data['questions'],
        )
        registration.save()
        return redirect('video_contest_thanks', video_contest_id=video_contest_id)
    else:
        return render(request, 'video_contest/form.html', {
            'home': False,
            'post': video_contest,
            'form': form,
            'header': get_header(request, video_contest, current='form'),
            'count_qualified': models.VideoContestRegistration.objects.filter(event=video_contest, qualified=True).count(),
        })


@handle_old_connections
def form(request, video_contest_id):
    if not request.user.is_authenticated:
        return redirect('video_contest_info', video_contest_id=video_contest_id)
    if request.method == 'POST':
        return form_post(request, video_contest_id)
    try:
        video_contest = models.VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    return render(request, 'video_contest/form.html', {
        'meta_title': '%s 報名表' % video_contest.title,
        'home': False,
        'user': request.user,
        'post': video_contest,
        'form': VideoContestRegistrationForm(video_contest, initial={'event': video_contest}),
        'header': get_header(request, video_contest, current='form'),
        'count_qualified': models.VideoContestRegistration.objects.filter(event=video_contest, qualified=True).count(),
    })


@handle_old_connections
def winners(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


def get_meta_tags_for_gallery_page(request, video_contest):
    meta_tags = {
        'og:url': request.build_absolute_uri(
            reverse('video_contest_gallery',
                    args=(video_contest.id, ))),
        'og:locale': 'zh_Hant',
        'og:type': 'website',
        'og:title': '%s 參賽影片' % video_contest.title,
        'og:description': video_contest.summary or '',
        'og:image': video_contest.cover_url or request.build_absolute_uri('static/img/logo.jpg'),
        'fb:app_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
    }
    return meta_tags


@handle_old_connections
def gallery(request, video_contest_id):
    try:
        video_contest = models.VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    groups = models.VideoContestGroup.objects.filter(video_contest=video_contest).order_by('name')

    return render(request, 'video_contest/gallery.html', {
        'meta_title': '%s 參賽影片' % video_contest.title,
        'meta_tags': get_meta_tags_for_gallery_page(request, video_contest),
        'home': False,
        'user': request.user,
        'video_contest': video_contest,
        'groups': groups,
        'registrations': {g.id: models.VideoContestRegistration.objects.filter(event=video_contest, group=g, qualified=True).order_by('-video_number') for g in groups},
        'header': get_header(request, video_contest, current='gallery'),
    })


def get_random_qualified_videos(video_contest, max_count):
    # FIXME: improve performance of getting random qualified videos
    videos = [v for v in models.VideoContestRegistration.objects.filter(event=video_contest, qualified=True).all()]
    total_count = len(videos)
    return sample(videos, max_count if total_count > max_count else total_count)


def get_modal_for_voting(request, video_contest):
    now = timezone.now()
    popup = False
    if now < video_contest.voting_start_time:
        popup = True
        body = '%s\n開放投票' % timezone.localtime(video_contest.voting_start_time).strftime('%Y/%m/%d %H:%M')
        actions = [{
            'name': '我知道了'
        }]
    elif now > video_contest.voting_end_time:
        popup = True
        body = '已截止投票'
        actions = [{
            'name': '我知道了'
        }]
    elif not request.user.is_authenticated:
        popup = True
        body = '要先登入才可投票喔！'
        actions = [{
            'name': '使用 Facebook 註冊／登入',
            'url': '{url}?next={next}'.format(
                    url=reverse('social:begin', args=('facebook',)),
                    next=request.path),
        }, {
            'name': '下次再說',
        }]
    if popup:
        return {
            'target': {
                'id': 'validation_before_voting',
            },
            'title': '李江却台語文教基金會',
            'body': body,
            'actions': actions
        }
    else:
        return None


def get_meta_tags_for_video_page(request, video_contest, registration):
    meta_tags = {
        'og:url': request.build_absolute_uri(
            reverse('video_contest_video',
                    args=(video_contest.id, registration.video_number))),
        'og:locale': 'zh_Hant',
        'og:type': 'website',
        'og:title': registration.video_title,
        'og:description': registration.introduction or '',
        'og:image': registration.cover_url,
        'fb:app_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
    }
    return meta_tags


@handle_old_connections
def video(request, video_contest_id, video_number):
    try:
        video_contest = models.VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    try:
        registration = models.VideoContestRegistration.objects.get(event=video_contest, video_number=video_number)
    except ObjectDoesNotExist:
        return redirect('home')

    is_voted = request.user.is_authenticated and request.user.profile.voted_videos.filter(id=registration.id).exists()
    videos = get_random_qualified_videos(video_contest, max_count=10)
    other_videos = [v for v in videos if v.id != registration.id]

    return render(request, 'video_contest/video.html', {
        'meta_title': '%s %s' % (video_contest.title, registration.video_title),
        'meta_tags': get_meta_tags_for_video_page(request, video_contest, registration),
        'home': False,
        'user': request.user,
        'layout': {
            'content': 'col-lg-8',
            'sidebar': 'col-lg-4',
        },
        'header_title': video_contest.title,
        'video_contest': video_contest,
        'video': registration,
        'other_videos': other_videos,
        'is_voted': is_voted,
        'vote_form': VideoContestVoteForm(initial={
            'method': 'DELETE' if is_voted else 'POST',
            'video_contest_registration_id': registration.id
        }),
        'header': get_header(request, video_contest, current='video'),
        'modal': get_modal_for_voting(request, video_contest)
    })


@login_required
@handle_old_connections
def vote(request, video_contest_id, video_number):
    if request.method != 'POST':
        return redirect('video_contest_video', video_contest_id=video_contest_id, video_number=video_number)

    vote_form = VideoContestVoteForm(data=request.POST)

    if not vote_form.is_valid():
        return redirect('video_contest_video', video_contest_id=video_contest_id, video_number=video_number)

    method = vote_form.cleaned_data['method']
    video_contest_registration_id = vote_form.cleaned_data['video_contest_registration_id']
    if method == 'POST':
        request.user.profile.voted_videos.add(video_contest_registration_id)
    elif method == 'DELETE':
        request.user.profile.voted_videos.remove(video_contest_registration_id)
    registration = models.VideoContestRegistration.objects.get(id=video_contest_registration_id)
    registration.votes = registration.voters.count()
    registration.save()
    return redirect('video_contest_video', video_contest_id=video_contest_id, video_number=video_number)


@handle_old_connections
def thanks(request, video_contest_id):
    try:
        video_contest = models.VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    return render(request, 'video_contest/thanks.html', {
        'home': False,
        'user': request.user,
        'video_contest_id': video_contest_id,
        'countdown': 10,
        'header': get_header(request, video_contest, current='thanks'),
    })
