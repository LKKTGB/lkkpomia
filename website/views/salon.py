from django.urls import reverse

from website.models.registration import Registration
from website.models.salon import Salon
from website.views.event import Event


class Salon(Event):
    template_name = 'salon.html'
    model = Salon

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['nav_items'] = [{
            'name': '活動內容',
            'link': reverse('post', kwargs={'post_id': self.object.id}),
            'current': True
        }]
        context_data['count_attendees'] = Registration.objects.filter(event=self.object).count()
        context_data['registration_modal'] = self.get_registration_modal()
        return context_data
