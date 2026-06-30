from django.shortcuts import render

def index(request):
    # This renders your dashboard HTML file
    return render(request, 'dashboard_test.html')
# Create your views here.
