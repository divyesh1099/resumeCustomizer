from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db import transaction

# Create your views here.
def index(requests):
    return render(requests, 'home/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:index')  # Assume there's a URL named 'home'
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    return redirect('home:login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Create the user's profile
                Profile.objects.create(user=user)
                
                # If additional profile data is being submitted, process it here
                # e.g., profile.phone_number = form.cleaned_data['phone_number']
                # Don't forget to save the profile after assigning the extra fields
                # profile.save()
                
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home:index')  # Assuming you have a 'home:index' URL
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'home/profile.html')

@login_required
def edit_profile_view(request):
    # Assume you have a form for editing the user profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home:profile')
    else:
        form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'home/edit_profile.html', {'form': form})
