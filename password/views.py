from django.shortcuts import render, redirect
from .models import NonCSV, Passwords
from django.contrib import messages
from .forms import PasswordForm
from django.http import JsonResponse
import random
import string
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



def password_generator(request):
    form = PasswordForm()
    return render(request, 'PasswordGenerator.html', {'form': form})

def generate_password_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        return JsonResponse({'password': password})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def passwordEntry(request):
    if request.method == 'POST':
        # process data
        usernameR = request.POST['username']
        passwordR = request.POST['password']

        user = NonCSV(username=usernameR, password=passwordR)
        if NonCSV.objects.filter(username=usernameR, password=passwordR).exists():
            return render(request, 'passwordEntry.html', {'usernameGet': usernameR})
        else:
            messages.error(request, 'USER NOT FOUND@!@##!#!#@@#$!@#!@#')
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

