from django.shortcuts import render


def dashboard(request):
    return render(request, "occ/dashboard.html")
# Create your views here.
