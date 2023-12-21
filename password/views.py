from django.shortcuts import render, redirect
from .models import NonCSV, Passwords
from django.contrib import messages
from .forms import PasswordForm
from django.http import JsonResponse
import random
import string


def landing(request):
    return render(request, 'landing.html')


def passwordEntry(request):
    # Get the username of the current user from the browser cache
    loginUserGet = request.session.get('usernameGet', '')
    if request.method == 'POST':
        # Extract data from the POST request
        username = request.POST.get('username')
        website = request.POST.get('website')
        password = request.POST.get('password')

        if request.POST.get('username') == '' or request.POST.get('website') == '' or request.POST.get(
                'password') == '':
            return JsonResponse({'status': 'error', 'type': 'empty', 'message': 'Empty Field!'}, status=400)
        else:

            if Passwords.objects.filter(name=loginUserGet, url=website, username=username, password=password).exists():
                return JsonResponse({'status': 'error', 'type': 'duplicate', 'message': 'Password already exists.'},
                                    status=400)

            # Assuming you're saving this data to a model
            user_data = Passwords(name=loginUserGet, username=username, url=website, password=password)
            user_data.save()

            # Return a JSON response indicating success
            return JsonResponse({'status': 'success'})

    return render(request, 'passwordEntry.html', {'usernameGet': loginUserGet})


def addDuplicate(request):
    loginUserGet = request.session.get('usernameGet', '')
    if request.method == 'POST':
        # Extract data from the POST request
        username = request.POST.get('username')
        website = request.POST.get('website')
        password = request.POST.get('password')
        user_data = Passwords(name=loginUserGet, username=username, url=website, password=password)
        user_data.save()
        return JsonResponse({'status': 'success'})


def password_generator(request):
    form = PasswordForm()
    return render(request, 'PasswordGenerator.html', {'form': form})


def generate_password_ajax(request):
    length = request.GET.get('length', 10)
    include_numbers = request.GET.get('include_numbers') == 'true'
    include_lowercase = request.GET.get('include_lowercase') == 'true'
    include_uppercase = request.GET.get('include_uppercase') == 'true'
    include_symbols = request.GET.get('include_symbols') == 'true'
    no_duplicates = request.GET.get('no_duplicates') == 'true'
    quantity = int(request.GET.get('quantity', 1))

    try:
        length = int(length)
        if length <= 0 or length > 100:  # Set maximum length as per your requirements
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'Invalid length'}, status=400)

    characters = ''
    if include_numbers:
        characters += string.digits
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_symbols:
        characters += string.punctuation

    if not characters:
        return JsonResponse({'error': 'No character types selected'}, status=400)

    passwords = []
    for _ in range(quantity):
        if no_duplicates:
            if len(characters) < length:
                return JsonResponse({'error': 'Not enough unique characters for the requested length'}, status=400)
            password = ''.join(random.sample(characters, length))
        else:
            password = ''.join(random.choice(characters) for _ in range(length))
        passwords.append(password)

    return JsonResponse({'passwords': passwords})


def loginLanding(request):
    if request.method == 'POST':
        # process data
        usernameR = request.POST['username']
        passwordR = request.POST['password']

        user = NonCSV(username=usernameR, password=passwordR)
        if NonCSV.objects.filter(username=usernameR, password=passwordR).exists():
            # Save the username of the Main user for later inside the browser session
            request.session['usernameGet'] = usernameR
            return render(request, 'loginLanding.html', {'usernameGet': usernameR})
        else:
            messages.error(request, 'User not found: Please try Again!')
            return redirect('login')


def passwordVault(request):
    return render(request, 'passwordVault.html')


def signUp(request):
    return render(request, 'signUp.html')


def login(request):
    if request.method == 'POST':
        usernameR = request.POST['username']
        passwordR = request.POST['password']

        user = NonCSV(username=usernameR, password=passwordR)
        user.save()
    return render(request, 'loginPage.html')
