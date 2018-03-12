from django.shortcuts import render

from website.models.privacy_policy import PrivacyPolicy
from website.utils import handle_old_connections


@handle_old_connections
def privacy(request):
    privacy_policy = PrivacyPolicy.get_solo()
    return render(request, 'privacy_policy.html', {
        'privacy_policy': privacy_policy
    })
