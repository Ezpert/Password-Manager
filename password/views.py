from django.shortcuts import render
from .models import NonCSV


def landing(request):
    return render(request, 'landing.html')


def getData(request):
    if request.method == 'POST':
        usernameR = request.POST['username']
        passwordR = request.POST['password']
        user = NonCSV(username=usernameR, password=passwordR)
        user.save()

    else:
        usernameR = 'NULL'

    return render(request, 'confirmation.html', {'usernameGet': usernameR})
