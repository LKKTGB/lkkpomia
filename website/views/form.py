from django.urls import reverse
from django.views.generic.edit import FormView

from website import models
from website.forms import SalonRegistrationForm


class SalonRegistrationFormView(FormView):
    template_name = 'salon/form.html'
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
