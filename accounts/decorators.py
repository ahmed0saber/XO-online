from django.shortcuts import redirect

def restrict_unlogged(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request,  *args, **kwargs)
        else:
            return redirect('app:home')
    return wrapper

def restrict_logged(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('app:home')
        else:
            return func(request,  *args, **kwargs)
    return wrapper
