from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homeapp:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            response = HttpResponseForbidden("Access denied: You are not allowed to access the requested page.")
            response['Refresh'] = f'3; url={reverse("homeapp:login")}'
            return response
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_student:
            return view_func(request, *args, **kwargs)
        else:
            response = HttpResponseForbidden("Access denied: You are not allowed to access the requested page.")
            response['Refresh'] = f'3; url={reverse("homeapp:login")}'
            return response
    return wrapper

def library_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_library:
            return view_func(request, *args, **kwargs)
        else:
            response = HttpResponseForbidden("Access denied: You are not allowed to access the requested page.")
            response['Refresh'] = f'3; url={reverse("homeapp:login")}'
            return response
    return wrapper

def finance_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_finance:
            return view_func(request, *args, **kwargs)
        else:
            response = HttpResponseForbidden("Access denied: You are not allowed to access the requested page.")
            response['Refresh'] = f'3; url={reverse("homeapp:login")}'
            return response
    return wrapper