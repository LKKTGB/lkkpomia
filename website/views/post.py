from django.conf import settings
from django.urls import reverse
from django.views.generic import DetailView

from website.views.page import Page


class Post(Page, DetailView):
    '''
    View for general blog post, just text and images.
    '''

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['login_modal'] = self.get_login_modal()
        context_data['meta_title'] = self.object.title,
        context_data['meta_tags'] = {
            'og:url': self.request.build_absolute_uri(reverse('post', args=(self.object.id,))),
            'og:locale': 'zh_Hant',
            'og:type': 'website',
            'og:title': self.object.title,
            'og:description': self.object.summary or '',
            'og:image': self.object.cover_url or self.request.build_absolute_uri('static/img/logo.jpg'),
            'fb:app_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
        }
        return context_data
