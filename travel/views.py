from django.shortcuts import render


def home(request):
    name = "Drake Hitch"
    return render(request, "home.html", {"name": name})
