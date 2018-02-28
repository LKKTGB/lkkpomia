from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from website.forms import VideoContestRegistrationForm, VideoContestVoteForm
from website.models.video_contest import VideoContest
from website.models.video_contest_group import VideoContestGroup
from website.models.video_contest_registration import VideoContestRegistration
from website.models.video_contest_winner import VideoContestWinner


def get_header(request, video_contest, current):
    now = timezone.now()
    headers = {}
    headers['活動內容'] = 'info'
    # headers['最新公告']= 'announcements'
    if now > video_contest.registration_start_time:
        headers['參賽影片'] = 'gallery'
        if VideoContestWinner.objects.filter(video_contest=video_contest).exists():
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
        'modal': {
            'target': {
                'id': 'header_modal',
            },
            'title': '李江却台語文教基金會',
            'body': '會員註冊或登入',
            'actions': [{
                    'name': '使用 Facebook 註冊／登入',
                    'url': '{url}?next={next}'.format(
                        url=reverse('social:begin', args=('facebook',)),
                        next=request.path),
            }, {
                'name': '下次再說',
            }]
        }
    }


def get_modal_for_registration(request, video_contest):
    now = timezone.now()
    if now < video_contest.registration_start_time:
        body = '%s 開放報名' % timezone.localtime(video_contest.registration_start_time).strftime('%Y/%m/%d %H:%M')
        actions = [{
            'name': '我知道了'
        }]
    elif now > video_contest.registration_end_time:
        body = '已截止報名'
        actions = [{
            'name': '我知道了'
        }]
    elif not request.user.is_authenticated:
        body = '要先登入才可報名喔！'
        actions = [{
            'name': '使用 Facebook 註冊／登入',
            'url': '{url}?next={next}'.format(
                    url=reverse('social:begin', args=('facebook',)),
                    next=reverse('video_contest_form', args=(video_contest.id,))),
        }, {
            'name': '下次再說',
        }]
    else:
        return None
    return {
        'target': {
            'id': 'validation_before_registration',
        },
        'title': '李江却台語文教基金會',
        'body': body,
        'actions': actions
    }


def get_meta_tags_for_info_page(request, video_contest):
    meta_tags = {
        'og:url': request.build_absolute_uri(reverse('video_contest_info', args=(video_contest.id,))),
        'og:locale': 'zh_Hant',
        'og:type': 'website',
        'og:title': video_contest.title,
        'og:description': video_contest.summary or '',
        'og:image': video_contest.cover_url or request.build_absolute_uri('static/img/logo.jpg'),
        'fb:app_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
    }
    return meta_tags


def info(request, video_contest_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)

    return render(request, 'video_contest/info.html', {
        'meta_tags': get_meta_tags_for_info_page(request, video_contest),
        'home': False,
        'user': request.user,
        'video_contest': video_contest,
        'header': get_header(request, video_contest, current='info'),
        # 'search': {
        #     'placeholder': '搜尋參賽影片'
        # },
        'count_qualified': VideoContestRegistration.objects.filter(event=video_contest, qualified=True).count(),
        'modal': get_modal_for_registration(request, video_contest)
    })


def announcements(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


@login_required
def form_post(request, video_contest_id):
    try:
        video_contest = VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    form = VideoContestRegistrationForm(data=request.POST, video_contest=video_contest)
    if form.is_valid():
        registration = VideoContestRegistration(
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
            'video_contest': video_contest,
            'form': form,
            'header': get_header(request, video_contest, current='form'),
            'count_qualified': VideoContestRegistration.objects.filter(event=video_contest, qualified=True).count(),
        })


def form(request, video_contest_id):
    if not request.user.is_authenticated:
        return redirect('video_contest_info', video_contest_id=video_contest_id)
    if request.method == 'POST':
        return form_post(request, video_contest_id)
    try:
        video_contest = VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    return render(request, 'video_contest/form.html', {
        'home': False,
        'user': request.user,
        'video_contest': video_contest,
        'form': VideoContestRegistrationForm(video_contest, initial={'event': video_contest}),
        'header': get_header(request, video_contest, current='form'),
        'count_qualified': VideoContestRegistration.objects.filter(event=video_contest, qualified=True).count(),
    })


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


def gallery(request, video_contest_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)
    groups = VideoContestGroup.objects.filter(video_contest=video_contest).order_by('name')

    return render(request, 'video_contest/gallery.html', {
        'meta_tags': get_meta_tags_for_gallery_page(request, video_contest),
        'home': False,
        'user': request.user,
        'video_contest': video_contest,
        'groups': groups,
        'registrations': {g.id: VideoContestRegistration.objects.filter(event=video_contest, group=g, qualified=True) for g in groups},
        'header': get_header(request, video_contest, current='gallery'),
    })


def get_random_qualified_videos(count):
    total_count = VideoContestRegistration.objects.count()
    ids = sample(list(range(total_count)), count if count < total_count else total_count)
    videos = [v for v in VideoContestRegistration.objects.filter(id__in=ids[:count], qualified=True).all()]
    return sample(videos, len(videos))


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


def video(request, video_contest_id, video_number):
    video_contest = VideoContest.objects.get(id=video_contest_id)
    registration = VideoContestRegistration.objects.get(event=video_contest, video_number=video_number)

    is_voted = request.user.is_authenticated and request.user.profile.voted_videos.filter(id=registration.id).exists()
    videos = get_random_qualified_videos(count=10)
    other_videos = [v for v in videos if v.id != registration.id]

    return render(request, 'video_contest/video.html', {
        'meta_tags': get_meta_tags_for_video_page(request, video_contest, registration),
        'home': False,
        'user': request.user,
        'layout': {
            'content': 'col-lg-8',
            'sidebar': 'col-lg-4',
        },
        'page_title': video_contest.title,
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
    registration = VideoContestRegistration.objects.get(id=video_contest_registration_id)
    registration.votes = registration.voters.count()
    registration.save()
    return redirect('video_contest_video', video_contest_id=video_contest_id, video_number=video_number)


def thanks(request, video_contest_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)
    return render(request, 'video_contest/thanks.html', {
        'home': False,
        'user': request.user,
        'video_contest_id': video_contest_id,
        'countdown': 10,
        'header': get_header(request, video_contest, current='thanks'),
    })
