from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm
from .decorators import redirect_authenticated_user
from django.contrib import messages
import secrets


@login_required(login_url='homeapp:login')
def IndexView(request):
    user = request.user

    context = {
        'Hello': 'Hello',
    }

    return render(request, 'index.html', context)


@login_required(login_url='homeapp:login')
def UserProfileView(request):
    user = request.user
    userform = UserForm(instance=user)

    if request.method == 'POST':
        if 'userform-submit' in request.POST:
            userform = UserForm(request.POST, instance=user)
            if userform.is_valid():
                userform.save()
                messages.success(request, 'Your information was successfully updated.')
                return redirect('homeapp:userprofile')

    context = {
        'userform': userform,
    }

    return render(request, 'userprofile.html', context)

@redirect_authenticated_user
def LoginView(request):
    if request.method == 'POST':
        loginform = LoginForm(data=request.POST)
        if loginform.is_valid():
            user = loginform.get_user()
            login(request, user)
            return redirect('homeapp:index')
    else:
        loginform = LoginForm()

    return render(request, 'login.html', {'loginform': loginform})


def LogoutView(request):
    logout(request)
    return redirect('homeapp:login')