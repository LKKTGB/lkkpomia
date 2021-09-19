from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormView

from website import models
from website.forms import DeleteForm, SalonRegistrationForm
from website.utils import format_time
from website.views.event import Event
from website.views.page import Page


def get_nav_items(salon, request):
    current_tab = resolve(request.path_info).url_name

    nav_items = []
    nav_items.append({
        'name': '活動內容',
        'link': reverse('post', kwargs={'post_id': salon.id}),
        'active': current_tab == 'post'
    })
    return nav_items


def get_sidebar_info(salon, request):
    info = [{
        'title': '活動時間',
        'body': '%s ~ %s' % (format_time(salon.start_time, 'YYYY/MM/DD HH:mm'), format_time(salon.end_time, 'HH:mm'))
    }, {
        'title': '入場時間',
        'body': format_time(salon.door_time, 'HH:mm')
    }, {
        'title': '活動地點',
        'body': salon.venue
    }, {
        'title': '活動地址',
        'body': salon.address
    }, {
        'title': '報名時間',
        'body': '%s ~ %s' % (format_time(salon.registration_start_time, 'YYYY/MM/DD HH:mm'),
                             format_time(salon.registration_end_time, 'YYYY/MM/DD HH:mm'))
    }]

    if salon.capacity > 0:
        info.append({
            'title': '報名狀況',
            'body': '%d／%d' % (salon.attendance(), salon.capacity)
        })

    now = timezone.now()
    started = now > salon.registration_start_time
    finished = now > salon.registration_end_time
    if started and not finished:
        info.append({
            'title': '點我報名',
            'link': reverse('form', kwargs={'post_id': salon.id}),
            'type': 'button'
        })
        if not request.user.is_anonymous and \
                models.SalonRegistration.objects.filter(event=salon.id, submitter=request.user).exists():
            info.append({
                'title': '取消報名',
                'link': reverse('forms', kwargs={'post_id': salon.id}),
                'type': 'button'
            })

    return info


class Salon(Event):
    template_name = 'event.html'
    model = models.Salon

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['header'] = {
            'title': self.object.title,
            'url': reverse('post', kwargs={'post_id': self.object.id})
        }
        context_data['nav_items'] = get_nav_items(self.object, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.object, self.request)
        context_data['registration_modal'] = self.get_registration_modal()
        return context_data


class SalonRegistrationFormView(FormView):
    template_name = 'event/form.html'
    form_class = SalonRegistrationForm
    salon = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.salon = models.Salon.objects.get(id=self.kwargs['pk'])
        kwargs.update({
            'salon': self.salon
        })
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['event'] = self.salon
        context_data['header'] = {
            'title': self.salon.title,
            'url': reverse('post', kwargs={'post_id': self.salon.id})
        }
        context_data['nav_items'] = get_nav_items(self.salon, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.salon, self.request)
        context_data['popup'] = self.get_popup()
        return context_data

    def get_success_url(self):
        return reverse('thanks', kwargs={'post_id': self.kwargs['pk']})

    def form_valid(self, form):
        registration = models.SalonRegistration(
            submitter=self.request.user,
            event=self.salon,
            contestant_name=form.cleaned_data['contestant_name'],
            phone_number=form.cleaned_data['phone_number'],
            email=form.cleaned_data['email'],
            attendance=form.cleaned_data['attendance'],
            other_attendees_info=form.cleaned_data['other_attendees_info']
        )
        registration.save()
        return super().form_valid(form)

    def get_popup(self):
        now = timezone.now()
        if now < self.salon.registration_start_time:
            body = '%s 開放報名' % timezone.localtime(self.salon.registration_start_time).strftime('%Y/%m/%d %H:%M')
            actions = [{
                'name': '我知道了',
                'url': reverse('post', args=(self.salon.id,))
            }]
        elif now > self.salon.registration_end_time:
            body = '已截止報名'
            actions = [{
                'name': '我知道了',
                'url': reverse('post', args=(self.salon.id,))
            }]
        elif self.salon.full_capacity():
            body = '名額已滿'
            actions = [{
                'name': '我知道了',
                'url': reverse('post', args=(self.salon.id,))
            }]
        elif not self.request.user.is_authenticated:
            body = '要先登入才可報名喔！'
            actions = [{
                'name': '使用 Facebook 註冊／登入',
                'url': '{url}?next={next}'.format(
                        url=reverse('social:begin', args=('facebook',)),
                        next=reverse('form', args=(self.salon.id,))),
            }, {
                'name': '下次再說',
                'url': reverse('post', args=(self.salon.id,))
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
            'redirect': reverse('post', args=(self.salon.id,))
        }


class SalonForms(Page, ListView):
    template_name = 'salon/forms.html'
    model = models.SalonRegistration

    salon = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        self.salon = models.Salon.objects.get(id=post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(event=self.salon, submitter=self.request.user).order_by('submit_time')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['login_modal'] = self.get_login_modal()
        context_data['header'] = {
            'title': self.salon.title,
            'url': reverse('post', kwargs={'post_id': self.salon.id})
        }
        context_data['nav_items'] = get_nav_items(self.salon, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.salon, self.request)
        context_data['delete_form'] = DeleteForm()
        return context_data


@login_required
def delete_form(request, post_id, form_id):
    if request.method != 'POST':
        return redirect('post', post_id=post_id)

    form = DeleteForm(data=request.POST)
    if not form.is_valid():
        return redirect('post', post_id=post_id)

    method = form.cleaned_data['method']
    if method != 'DELETE':
        return redirect('post', post_id=post_id)

    try:
        registration = models.SalonRegistration.objects.filter(event=post_id, submitter=request.user).get(id=form_id)
        registration.delete()
    except ObjectDoesNotExist:
        return redirect('post', post_id=post_id)

    if models.SalonRegistration.objects.filter(event=post_id, submitter=request.user).exists():
        return redirect('forms', post_id=post_id)
    else:
        return redirect('post', post_id=post_id)
