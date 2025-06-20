from django.views import View
from django.shortcuts import render


def index(request):
    context = {
        'title': 'Main Page'
    }

    return render(request, 'index.html', context)