from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse

from website.forms import VideoContestRegistrationForm
from website.models.video_contest import VideoContest
from website.models.video_contest_group import VideoContestGroup
from website.models.video_contest_registration import VideoContestRegistration


def nav_items(request, video_contest_id):
    return [{
        'name': '活動內容',
        'link': reverse('video_contest_info', kwargs={'video_contest_id': video_contest_id}),
        'current': True
    }, {
        'name': '最新公告',
        'link': reverse('video_contest_announcements', kwargs={'video_contest_id': video_contest_id}),
        'current': False
    }, {
        'name': '得獎影片',
        'link': reverse('video_contest_winners', kwargs={'video_contest_id': video_contest_id}),
        'current': False
    }, {
        'name': '參賽影片',
        'link': reverse('video_contest_gallery', kwargs={'video_contest_id': video_contest_id}),
        'current': False
    }]


def info(request, video_contest_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)

    return render(request, 'video_contest/info.html', {
        'video_contest': video_contest,
        'nav_items': nav_items(request, video_contest_id),
        'registrations': [{
            'submitter': {
                'profile': {
                    'avatar_url': 'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e15/11352284_1704356839787218_67514963_n.jpg'
                }
            }
        } for _ in range(20)],
        'rest_submitters': 10,
        'search': {
            'placeholder': '搜尋參賽影片'
        }
    })


def announcements(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


@login_required
def form(request, video_contest_id):
    if request.method == 'POST':
        return redirect('video_contest_info', video_contest_id=video_contest_id)
    try:
        video_contest = VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    return render(request, 'video_contest/form.html', {
        'video_contest': video_contest,
        'form': VideoContestRegistrationForm(video_contest),
        'nav_items': nav_items(request, video_contest_id),
    })


def winners(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


def gallery(request, video_contest_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)
    groups = VideoContestGroup.objects.filter(video_contest=video_contest).order_by('name')

    return render(request, 'video_contest/gallery.html', {
        'video_contest': video_contest,
        'groups': groups,
        'registrations': {g.id: VideoContestRegistration.objects.filter(event=video_contest, group=g, qualified=True) for g in groups},
        'nav_items': nav_items(request, video_contest_id),
    })


def video(request, video_contest_id, video_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)
    registration = VideoContestRegistration.objects.get(id=video_id)

    return render(request, 'video_contest/video.html', {
        'video_contest': video_contest,
        'video': registration,
        'other_videos': VideoContestRegistration.objects.filter(event=video_contest, group=registration.group, qualified=True),
        'nav_items': nav_items(request, video_contest_id),
    })
