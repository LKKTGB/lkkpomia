from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def video_contest_registration(request, video_contest_id):
    return redirect('video_contest_info', video_contest_id=video_contest_id)
