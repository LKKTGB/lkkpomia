from django.shortcuts import redirect


def home(request):
    return redirect('video_contest_info', video_contest_id=1)
