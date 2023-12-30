from django.shortcuts import render, redirect, get_object_or_404
from .models import NonCSV, Passwords
from django.contrib import messages
from .forms import PasswordForm
from django.http import JsonResponse
import random
import string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
            request.session['usernameGet'] = usernameR
            # Save the username of the Main user for later inside the browser session
            return render(request, 'loginLanding.html', {'usernameGet': usernameR})
        else:
            messages.error(request, 'User not found: Please try Again!')
            return redirect('login')

    usernameR = request.session.get('usernameGet', '')
    return render(request, 'loginLanding.html', {'usernameGet': usernameR})


def passwordVault(request, message=None):
    # Your existing code here...
    loginUserGet = request.session.get('usernameGet', '')
    # Query the database for all entries that match the adminUser
    entries = Passwords.objects.filter(name=loginUserGet)

    return render(request, 'passwordVault.html', {'entries': entries, 'adminUser': loginUserGet})


@csrf_exempt
def delete_entry(request, entry_id):
    try:
        Passwords.objects.get(id=entry_id).delete()
        return JsonResponse({'status': 'success'})
    except Passwords.DoesNotExist:
        return JsonResponse({'status': 'error'})


def editEntry(request, entryid):
    print("editEntry start")
    # Your existing code here...

    if request.method == 'POST':
        entry = Passwords.objects.get(id=entryid)
        if 'username' in request.POST:
            newUser = request.POST['username']
        else:
            newUser = entry.username  # Keep the old username
        if 'password' in request.POST:
            newPass = request.POST['password']
        else:
            newPass = entry.password  # Keep the old password

        # Update the username
        entry.username = newUser
        entry.password = newPass

        # Save the changes to the database
        entry.save()

        return redirect('passwordVault')


def editPage(request, entryid):
    # When you use filter(), it returns a QuerySet, which can contain multiple objects.
    # Even if there's only one matching object, it's still returned inside a QuerySet.
    # When you're trying to access entry.url, entry.username, and entry.password in your template,
    # Django is looking for url, username, and password attributes on the QuerySet itself, not on the objects inside it.
    # If you're sure that there will only be one object with the given id, you can use get() instead of filter().
    # get() returns a single object directly, not a QuerySet:
    entry = Passwords.objects.get(id=entryid)

    return render(request, 'editPage.html', {'entry': entry})


def signUp(request):
    return render(request, 'signUp.html')


def login(request):
    if request.method == 'POST':
        usernameR = request.POST['username']
        passwordR = request.POST['password']

        user = NonCSV(username=usernameR, password=passwordR)
        user.save()
    return render(request, 'loginPage.html')
