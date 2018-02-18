from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse

from website.forms import VideoContestRegistrationForm
from website.models.video_contest import VideoContest
from website.models.video_contest_group import VideoContestGroup
from website.models.video_contest_registration import VideoContestRegistration


def nav_items(request, video_contest_id, current):
    items = []
    for name, view in {
            '活動內容': 'info',
            '最新公告': 'announcements',
            '得獎影片': 'winners',
            '參賽影片': 'gallery'}.items():
        items.append({
            'name': name,
            'link': reverse('video_contest_%s' % view, kwargs={'video_contest_id': video_contest_id}),
            'current': view == current
        })
    return items


def info(request, video_contest_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)

    return render(request, 'video_contest/info.html', {
        'home': False,
        'user': request.user,
        'video_contest': video_contest,
        'nav_items': nav_items(request, video_contest_id, current='info'),
        'search': {
            'placeholder': '搜尋參賽影片'
        },
        'count_qualified': VideoContestRegistration.objects.filter(event=video_contest, qualified=True).count(),
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
            # FIXME: check youtube_id, not url
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
            'nav_items': nav_items(request, video_contest_id, current='form'),
        })


@login_required
def form(request, video_contest_id):
    if request.method == 'POST':
        return form_post(request, video_contest_id)
    try:
        video_contest = VideoContest.objects.get(id=video_contest_id)
    except ObjectDoesNotExist:
        return redirect('home')

    return render(request, 'video_contest/form.html', {
        'home': False,
        'video_contest': video_contest,
        'form': VideoContestRegistrationForm(video_contest),
        'nav_items': nav_items(request, video_contest_id, current='form'),
    })


def winners(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


def gallery(request, video_contest_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)
    groups = VideoContestGroup.objects.filter(video_contest=video_contest).order_by('name')

    return render(request, 'video_contest/gallery.html', {
        'home': False,
        'video_contest': video_contest,
        'groups': groups,
        'registrations': {g.id: VideoContestRegistration.objects.filter(event=video_contest, group=g, qualified=True) for g in groups},
        'nav_items': nav_items(request, video_contest_id, current='gallery'),
    })


def video(request, video_contest_id, video_id):
    video_contest = VideoContest.objects.get(id=video_contest_id)
    registration = VideoContestRegistration.objects.get(id=video_id)

    return render(request, 'video_contest/video.html', {
        'home': False,
        'video_contest': video_contest,
        'video': registration,
        'other_videos': VideoContestRegistration.objects.filter(event=video_contest, group=registration.group, qualified=True),
        'nav_items': nav_items(request, video_contest_id, current='video'),
    })


def thanks(request, video_contest_id):
    return render(request, 'video_contest/thanks.html', {
        'home': False,
        'video_contest_id': video_contest_id,
        'countdown': 10,
        'nav_items': nav_items(request, video_contest_id, current='thanks'),
    })
