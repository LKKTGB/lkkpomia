from django.utils import timezone
from django.urls import reverse


def get_registration_modal(request, event):
    now = timezone.now()
    if now < event.registration_start_time:
        body = '%s 開放報名' % timezone.localtime(event.registration_start_time).strftime('%Y/%m/%d %H:%M')
        actions = [{
            'name': '我知道了'
        }]
    elif now > event.registration_end_time:
        body = '已截止報名'
        actions = [{
            'name': '我知道了'
        }]
    elif not request.user.is_authenticated:
        body = '要先登入才可報名喔！'
        actions = [{
            'name': '使用 Facebook 註冊／登入',
            'url': '{url}?next={next}'.format(
                    url=reverse('social:begin', args=('facebook',)),
                    next=reverse('video_contest_form', args=(event.id,))),
        }, {
            'name': '下次再說',
        }]
    else:
        return None
    return {
        'target': {
            'id': 'validation_before_registration',
        },
        'title': '李江却台語文教基金會',
        'body': body,
        'actions': actions
    }
