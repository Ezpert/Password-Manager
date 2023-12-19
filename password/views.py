from django.shortcuts import render, redirect
from .models import NonCSV, Passwords
from django.contrib import messages
from .forms import PasswordForm

def landing(request):
    return render(request, 'landing.html')


def getData(request):
    if request.method == 'POST':
        usernameR = request.POST['username']
        websiteR = request.POST['website']
        passwordR = request.POST['password']
        user = Passwords(url=websiteR, username=usernameR, password=passwordR)
        user.save()

    else:
        usernameR = 'NULL'

    return render(request, 'confirmation.html', {'usernameGet': usernameR})

def generate_password(request):
    form = PasswordForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password']
    else:
        password = ''
    return render(request, 'PasswordGenerator.html', {'form': form, 'password': password})


def passwordEntry(request):
    if request.method == 'POST':
        # process data
        usernameR = request.POST['username']
        passwordR = request.POST['password']

        user = NonCSV(username=usernameR, password=passwordR)
        if NonCSV.objects.filter(username=usernameR, password=passwordR).exists():
            return render(request, 'passwordEntry.html', {'usernameGet': usernameR})
        else:
            messages.error(request, 'User not found: Please try Again!')
            return redirect('login')


def signUp(request):
    return render(request, 'signUp.html')


def login(request):
    if request.method == 'POST':
        usernameR = request.POST['username']
        passwordR = request.POST['password']

        user = NonCSV(username=usernameR, password=passwordR)
        user.save()
    return render(request, 'loginPage.html')
