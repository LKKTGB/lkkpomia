from collections import OrderedDict
from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.template.defaultfilters import date
from django.urls import resolve, reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from website import models
from website.forms import VideoContestRegistrationForm, VideoContestVoteForm
from website.utils import handle_old_connections
from website.views.base import get_login_modal
from website.views.event import Event
from website.views.page import Page
from website.views.post import Post


def get_nav_items(video_contest, request):
    now = timezone.now()
    contest_started = now > video_contest.registration_start_time
    winners_announced = models.VideoContestWinner.objects.filter(video_contest=video_contest).exists()
    registration_finished = now > video_contest.registration_end_time

    current_tab = resolve(request.path_info).url_name

    nav_items = []
    nav_items.append({
        'name': '活動內容',
        'link': reverse('post', kwargs={'post_id': video_contest.id}),
        'active': current_tab == 'post'
    })
    if not registration_finished:
        nav_items.append({
            'name': '我要報名',
            'link': reverse('form', kwargs={'post_id': video_contest.id}),
            'active': current_tab == 'form'
        })
    if contest_started:
        nav_items.append({
            'name': '參賽影片',
            'link': reverse('gallery', kwargs={'post_id': video_contest.id}),
            'active': current_tab == 'gallery'
        })
    if contest_started and winners_announced:
        nav_items.append({
            'name': '得獎影片',
            'link': reverse('winners', kwargs={'post_id': video_contest.id}),
            'active': current_tab == 'winners'
        })
    return nav_items


def get_sidebar_info(video_contest):
    info = OrderedDict()
    info['活動時間'] = '%s ~ %s' % (date(video_contest.start_time, 'Y/m/d'), date(video_contest.end_time, 'Y/m/d'))
    info['報名時間'] = '%s ~ %s' % (date(video_contest.registration_start_time, 'Y/m/d H:i'),
                                date(video_contest.registration_end_time, 'Y/m/d H:i'))
    info['投票時間'] = '%s ~ %s' % (date(video_contest.voting_start_time, 'Y/m/d H:i'),
                                date(video_contest.voting_end_time, 'Y/m/d H:i'))
    return info


class VideoContest(Event):
    template_name = 'event.html'
    model = models.VideoContest

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['header'] = {
            'title': self.object.title,
            'url': reverse('post', kwargs={'post_id': self.object.id})
        }
        context_data['search'] = {
            'target': reverse('gallery', kwargs={'post_id': self.object.id}),
            'placeholder': '搜尋影片'
        }
        context_data['nav_items'] = get_nav_items(self.object, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.object)
        context_data['registration_modal'] = self.get_registration_modal()
        return context_data


class VideoContestRegistrationFormView(FormView):
    template_name = 'event/form.html'
    form_class = VideoContestRegistrationForm
    video_contest = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.video_contest = models.VideoContest.objects.get(id=self.kwargs['pk'])
        kwargs.update({
            'video_contest': self.video_contest,
        })
        kwargs['initial'].update({
            'event': self.video_contest
        })
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['event'] = self.video_contest
        context_data['header'] = {
            'title': self.video_contest.title,
            'url': reverse('post', kwargs={'post_id': self.video_contest.id})
        }
        context_data['nav_items'] = get_nav_items(self.video_contest, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.video_contest)
        context_data['promises'] = [
            '本人同意主辦單位基於宣傳及存證等需要下載、再製或再利用參賽之影片。',
            '本人已瞭解並同意大會規定（大會規定請見活動簡章），若入選評審獎，需配合出席頒獎典禮，方能領取獎勵金，否則視為棄權。',
            '上述資料皆正確無誤。'
        ]
        context_data['popup'] = self.get_popup()
        return context_data

    def get_success_url(self):
        return reverse('video_contest_thanks', kwargs={'video_contest_id': self.kwargs['pk']})

    def form_valid(self, form):
        registration = models.VideoContestRegistration(
            submitter=self.request.user,
            event=self.video_contest,
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
        return super().form_valid(form)

    def get_popup(self):
        now = timezone.now()
        if now < self.video_contest.registration_start_time:
            body = '%s 開放報名' % timezone.localtime(self.video_contest.registration_start_time).strftime('%Y/%m/%d %H:%M')
            actions = [{
                'name': '我知道了',
                'url': reverse('post', args=(self.video_contest.id,))
            }]
        elif now > self.video_contest.registration_end_time:
            body = '已截止報名'
            actions = [{
                'name': '我知道了',
                'url': reverse('post', args=(self.video_contest.id,))
            }]
        elif not self.request.user.is_authenticated:
            body = '要先登入才可報名喔！'
            actions = [{
                'name': '使用 Facebook 註冊／登入',
                'url': '{url}?next={next}'.format(
                        url=reverse('social:begin', args=('facebook',)),
                        next=reverse('form', args=(self.video_contest.id,))),
            }, {
                'name': '下次再說',
                'url': reverse('post', args=(self.video_contest.id,))
            }]
        else:
            return None
        return {
            'target': {
                'id': 'form_popup',
            },
            'title': '李江却台語文教基金會',
            'body': body,
            'actions': actions,
            'redirect': reverse('post', args=(self.video_contest.id,))
        }


class Gallery(Page, ListView):
    template_name = 'video_contest/gallery.html'
    model = models.VideoContestRegistration

    # TODO: Enable paging
    allow_empty = True
    ordering = '-video_number'

    video_contest = None
    keyword = None
    groups = None
    current_group = None

    def dispatch(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        self.video_contest = models.VideoContest.objects.get(id=post_id)
        self.groups = models.VideoContestGroup.objects.filter(video_contest=self.video_contest).order_by('name')

        self.keyword = self.request.GET.get('search', None)
        if not self.keyword:
            # redirect to first group
            try:
                self.current_group = models.VideoContestGroup.objects.get(name=self.request.GET.get('group', None))
            except ObjectDoesNotExist:
                return redirect(reverse('gallery', kwargs=kwargs) + '?group=%s' % self.groups[0].name)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.keyword:
            return self.model.objects.filter(event=self.video_contest, qualified=True, video_title__icontains=self.keyword)
        else:
            return self.model.objects.filter(event=self.video_contest, qualified=True, group=self.current_group)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['login_modal'] = self.get_login_modal()
        context_data['meta_title'] = '李江却台語文教基金會'
        context_data['meta_tags'] = {
            'og:url': self.request.build_absolute_uri(),
            'og:locale': 'zh_Hant',
            'og:type': 'website',
            'og:title': '%s 參賽影片' % self.video_contest.title,
            'og:description': self.video_contest.summary or '',
            'og:image': self.video_contest.cover_url or self.request.build_absolute_uri('static/img/logo.jpg'),
            'fb:app_id': settings.SOCIAL_AUTH_FACEBOOK_KEY
        }
        context_data['header'] = {
            'title': self.video_contest.title,
            'url': reverse('post', kwargs={'post_id': self.video_contest.id})
        }
        context_data['search'] = {
            'target': reverse('gallery', kwargs={'post_id': self.video_contest.id}),
            'placeholder': '搜尋影片'
        }
        context_data['nav_items'] = get_nav_items(self.video_contest, self.request)
        context_data['video_contest'] = self.video_contest
        context_data['groups'] = self.groups
        context_data['current_group'] = self.current_group
        context_data['keyword'] = self.keyword

        return context_data


class Winners(Page, ListView):
    template_name = 'video_contest/winners.html'
    model = models.VideoContestWinner

    allow_empty = True
    # ordering = '-video_number'
    # paginate_by = 20
    # paginate_orphans = 30

    video_contest = None

    def dispatch(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        self.video_contest = models.VideoContest.objects.get(id=post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(video_contest=self.video_contest).order_by('order')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['login_modal'] = self.get_login_modal()
        context_data['meta_title'] = '%s 得獎者' % self.video_contest.title
        context_data['meta_tags'] = {
            'og:url': self.request.build_absolute_uri(),
            'og:locale': 'zh_Hant',
            'og:type': 'website',
            'og:title': '%s 得獎者' % self.video_contest.title,
            'og:description': self.video_contest.summary or '',
            'og:image': self.video_contest.cover_url or self.request.build_absolute_uri('static/img/logo.jpg'),
            'fb:app_id': settings.SOCIAL_AUTH_FACEBOOK_KEY
        }
        context_data['header'] = {
            'title': self.video_contest.title,
            'url': reverse('post', kwargs={'post_id': self.video_contest.id})
        }
        context_data['search'] = {
            'target': reverse('gallery', kwargs={'post_id': self.video_contest.id}),
            'placeholder': '搜尋影片'
        }
        context_data['nav_items'] = get_nav_items(self.video_contest, self.request)
        context_data['video_contest'] = self.video_contest
        context_data['prizes'] = self.get_prizes()
        return context_data

    def get_prizes(self):
        prizes = OrderedDict()
        for winner in self.object_list:
            if winner.prize not in prizes:
                prizes[winner.prize] = []
            prizes[winner.prize].append(winner)
        return prizes


class Video(Page, DetailView):
    template_name = 'video_contest/video.html'
    model = models.VideoContestRegistration

    video_contest = None

    def dispatch(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        self.video_contest = models.VideoContest.objects.get(id=post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return models.VideoContestRegistration.objects.get(event=self.video_contest, video_number=self.kwargs['video_number'])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['login_modal'] = self.get_login_modal()
        context_data['meta_title']: '%s %s' % (self.video_contest.title, self.object.video_title)
        context_data['meta_tags'] = self.get_meta_tags()
        context_data['header'] = {
            'title': self.video_contest.title,
            'url': reverse('post', kwargs={'post_id': self.video_contest.id})
        }
        context_data['search'] = {
            'target': reverse('gallery', kwargs={'post_id': self.video_contest.id}),
            'placeholder': '搜尋影片'
        }
        context_data['nav_items'] = get_nav_items(self.video_contest, self.request)

        videos = self.get_random_qualified_videos(max_count=10)
        is_voted = self.request.user.is_authenticated and self.request.user.profile.voted_videos.filter(
            id=self.object.id).exists()
        context_data['other_videos'] = [v for v in videos if v.id != self.object.id]
        context_data['header_title'] = self.video_contest.title
        context_data['video_contest'] = self.video_contest
        context_data['is_voted'] = is_voted
        context_data['vote_form'] = VideoContestVoteForm(initial={
            'method': 'DELETE' if is_voted else 'POST',
            'video_contest_registration_id': self.object.id
        })
        context_data['voting_modal'] = self.get_voting_modal()
        return context_data

    def get_meta_tags(self):
        meta_tags = {
            'og:url': self.request.build_absolute_uri(),
            'og:locale': 'zh_Hant',
            'og:type': 'website',
            'og:title': self.object.video_title,
            'og:description': self.object.introduction or '',
            'og:image': self.object.cover_url,
            'fb:app_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
        }
        return meta_tags

    def get_random_qualified_videos(self, max_count):
        # FIXME: improve performance of getting random qualified videos
        videos = [v for v in models.VideoContestRegistration.objects.filter(
            event=self.video_contest, qualified=True).all()]
        total_count = len(videos)
        return sample(videos, max_count if total_count > max_count else total_count)

    def get_voting_modal(self):
        now = timezone.now()
        popup = False
        if now < self.video_contest.voting_start_time:
            popup = True
            body = '%s\n開放投票' % timezone.localtime(self.video_contest.voting_start_time).strftime('%Y/%m/%d %H:%M')
            actions = [{
                'name': '我知道了'
            }]
        elif now > self.video_contest.voting_end_time:
            popup = True
            body = '已截止投票'
            actions = [{
                'name': '我知道了'
            }]
        elif not self.request.user.is_authenticated:
            popup = True
            body = '要先登入才可投票喔！'
            actions = [{
                'name': '使用 Facebook 註冊／登入',
                'url': '{url}?next={next}'.format(
                        url=reverse('social:begin', args=('facebook',)),
                        next=self.request.path),
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


class Thanks(Post):
    template_name = 'video_contest/thanks.html'
    model = models.VideoContest

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['header'] = {
            'title': self.object.title,
            'url': reverse('post', kwargs={'post_id': self.object.id})
        }
        context_data['nav_items'] = get_nav_items(self.object, self.request)
        context_data['post_id'] = self.object.id
        context_data['countdown'] = 10
        return context_data


def info(request, video_contest_id):
    return redirect('post', post_id=video_contest_id)


@handle_old_connections
def announcements(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


@handle_old_connections
def winners(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=1)


def gallery(request, video_contest_id):
    return redirect('gallery', post_id=video_contest_id)


def video(request, video_contest_id, video_number):
    return redirect('video', post_id=video_contest_id, video_number=video_number)


@login_required
def vote(request, post_id, video_number):
    if request.method != 'POST':
        return redirect('video', post_id=post_id, video_number=video_number)

    vote_form = VideoContestVoteForm(data=request.POST)

    if not vote_form.is_valid():
        return redirect('video', post_id=post_id, video_number=video_number)

    method = vote_form.cleaned_data['method']
    video_contest_registration_id = vote_form.cleaned_data['video_contest_registration_id']
    if method == 'POST':
        request.user.profile.voted_videos.add(video_contest_registration_id)
    elif method == 'DELETE':
        request.user.profile.voted_videos.remove(video_contest_registration_id)
    registration = models.VideoContestRegistration.objects.get(id=video_contest_registration_id)
    registration.votes = registration.voters.count()
    registration.save()
    return redirect('video', post_id=post_id, video_number=video_number)
