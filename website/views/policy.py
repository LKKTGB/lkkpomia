from django.shortcuts import render

from website.models.privacy_policy import PrivacyPolicy


def privacy(request):
    privacy_policy = PrivacyPolicy.get_solo()
    return render(request, 'privacy_policy.html', {
        'privacy_policy': privacy_policy
    })
