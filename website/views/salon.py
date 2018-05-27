from collections import OrderedDict

from django.template.defaultfilters import date, time
from django.urls import resolve, reverse
from django.views.generic.edit import FormView

from website import models
from website.forms import SalonRegistrationForm
from website.views.event import Event


def get_nav_items(salon, request):
    current_tab = resolve(request.path_info).url_name

    nav_items = []
    nav_items.append({
        'name': '活動內容',
        'link': reverse('post', kwargs={'post_id': salon.id}),
        'current': current_tab == 'post'
    })
    return nav_items


def get_sidebar_info(salon):
    info = OrderedDict()
    info['活動時間'] = '%s %s~%s' % (date(salon.start_time, 'Y/m/d'), time(salon.start_time), time(salon.end_time))
    info['入場時間'] = time(salon.door_time)
    info['活動地點'] = salon.venue
    info['活動地址'] = salon.address
    info['報名時間'] = '%s ~ %s' % (date(salon.registration_start_time, 'Y/m/d H:i'),
                                date(salon.registration_end_time, 'Y/m/d H:i'))
    info['報名狀況'] = '已有 %d 人報名參加' % models.SalonRegistration.objects.filter(event=salon).count()
    return info


class Salon(Event):
    template_name = 'event.html'
    model = models.Salon

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['nav_items'] = get_nav_items(self.object, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.object)
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
        context_data['nav_items'] = get_nav_items(self.salon, self.request)
        context_data['sidebar_info'] = get_sidebar_info(self.salon)
        return context_data

    def get_success_url(self):
        return reverse('thanks', kwargs={'post_id': self.kwargs['pk']})

    def form_valid(self, form):
        registration = models.SalonRegistration(
            submitter=self.request.user,
            event=self.salon,
            contestant_name=form.cleaned_data['contestant_name'],
            phone_number=form.cleaned_data['phone_number'],
            email=form.cleaned_data['email']
        )
        registration.save()
        return super().form_valid(form)
