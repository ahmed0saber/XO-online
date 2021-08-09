from django.shortcuts import redirect

def restrict_unlogged(next):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request,  *args, **kwargs)
            else:
                return redirect('accounts:signup', next)
        return wrapper
    return decorator


def restrict_logged(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('app:home')
        else:
            return func(request,  *args, **kwargs)
    return wrapper
