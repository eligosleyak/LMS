# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterUserForm, UserUpdateForm, PasswordChangeForm  # Fix the import statement
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

def register_rider(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_rider = True
            var.save()
            messages.success(request, 'Account created for rider')
            return redirect('dashboard')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f'{field.capitalize()}: {error}')
            return redirect('register-rider')
    else:
        form = RegisterUserForm()
        context = {'form': form}
        return render(request, 'users/register_rider.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, f'You are logged in as {user}')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Session ended. Please, log in to continue')
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit-profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'password_form': password_form})
