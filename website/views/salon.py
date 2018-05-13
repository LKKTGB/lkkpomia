from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse

from website import models
from website.forms import SalonRegistrationForm
from website.views.event import Event


class Salon(Event):
    template_name = 'salon.html'
    model = models.Salon

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['nav_items'] = [{
            'name': '活動內容',
            'link': reverse('post', kwargs={'post_id': self.object.id}),
            'current': True
        }]
        context_data['count_attendees'] = self.object.attendees.count()
        context_data['registration_modal'] = self.get_registration_modal()
        context_data['is_registered'] = self.request.user.is_authenticated and self.request.user.profile.registered_salons.filter(
            id=self.object.id).exists()
        context_data['registration_form'] = SalonRegistrationForm(initial={
            'method': 'DELETE' if context_data['is_registered'] else 'POST',
            'salon_id': self.object.id
        })
        return context_data


@login_required
def register(request, post_id):
    if request.method != 'POST':
        return redirect('post', post_id=post_id)
    try:
        models.Salon.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect('home')

    form = SalonRegistrationForm(data=request.POST)

    if not form.is_valid():
        return redirect('post', post_id=post_id)

    method = form.cleaned_data['method']
    if method == 'POST':
        request.user.profile.registered_salons.add(post_id)
    elif method == 'DELETE':
        request.user.profile.registered_salons.remove(post_id)
    return redirect('post', post_id=post_id)
