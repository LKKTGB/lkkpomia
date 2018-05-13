from django.shortcuts import render

from website import models
from website.utils import handle_old_connections


@handle_old_connections
def privacy(request):
    privacy_policy = models.PrivacyPolicy.get_solo()
    return render(request, 'privacy_policy.html', {
        'privacy_policy': privacy_policy
    })
