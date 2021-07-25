from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'app/start.html')

def about(request):
    return render(request, 'app/about.html')