from django.shortcuts import render
from .models import Passwords


def landing(request):
    return render(request, 'landing.html')


def getData(request):
    if request.method == 'POST':
        usernameR = request.POST['username']
        passwordR = request.POST['password']
        user = Passwords(username=usernameR, password=passwordR)
        user.save()

    return render(request, 'confirmation.html', {'usernameR': 'usernameR'})
