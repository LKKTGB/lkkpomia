from django.urls import reverse
from django.views.generic.base import TemplateView


class Page(TemplateView):
    '''
    Base view for web pages
    '''
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['login_modal'] = {
            'target': {
                'id': 'header_modal',
            },
            'title': '李江却台語文教基金會',
            'body': '會員註冊或登入',
            'actions': [{
                    'name': '使用 Facebook 註冊／登入',
                        'url': '{url}?next={next}'.format(
                            url=reverse('social:begin', args=('facebook',)),
                            next=self.request.path),
                        }, {
                    'name': '下次再說',
            }]
        }
        return context_data
