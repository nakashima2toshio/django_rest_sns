from django.shortcuts import redirect


def redirect_to_sns_app(request):
    return redirect('/sns_app/')
