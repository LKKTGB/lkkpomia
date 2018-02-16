from django.shortcuts import redirect, render
from django.urls import reverse

from website.models.video_contest import VideoContest


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


def form(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


def winners(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


def gallery(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


def video(request, video_contest_id, video_id):
    return redirect('video_contest_info', video_contest_id=1)
