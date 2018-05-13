from django.urls import reverse


class Page:
    '''
    Base view for web pages
    '''

    def get_login_modal(self, **kwargs):
        return {
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
