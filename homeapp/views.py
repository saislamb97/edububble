from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm
from .decorators import redirect_authenticated_user, admin_required, student_required, library_required, finance_required
from django.contrib import messages
import secrets


@login_required(login_url='homeapp:login')
@admin_required
def IndexView(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'index.html', context)

@login_required(login_url='homeapp:login')
@student_required
def StudentIndexView(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'student/student_index.html', context)

@login_required(login_url='homeapp:login')
@student_required
def StudentTextbookView(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'student/student_textbook.html', context)

@login_required(login_url='homeapp:login')
@student_required
def StudentPaymentView(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'student/student_payment.html', context)

@login_required(login_url='homeapp:login')
@library_required
def LibraryIndexView(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'library/library_index.html', context)

@login_required(login_url='homeapp:login')
@finance_required
def FinanceIndexView(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'finance/finance_index.html', context)


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

def LoginView(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('homeapp:index')
        elif request.user.is_student:
            return redirect('homeapp:student_index')
        elif request.user.is_library:
            return redirect('homeapp:library_index')
        elif request.user.is_finance:
            return redirect('homeapp:finance_index')
        else:
            return redirect('homeapp:index')

    if request.method == 'POST':
        loginform = LoginForm(data=request.POST)
        if loginform.is_valid():
            user = loginform.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('homeapp:index')
            elif user.is_student:
                return redirect('homeapp:student_index')
            elif user.is_library:
                return redirect('homeapp:library_index')
            elif user.is_finance:
                return redirect('homeapp:finance_index')
            else:
                return redirect('homeapp:index')
    else:
        loginform = LoginForm()

    return render(request, 'login.html', {'loginform': loginform})


def LogoutView(request):
    logout(request)
    return redirect('homeapp:login')