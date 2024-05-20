from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from ..utils import get_mongodb


def home(request):
    db = get_mongodb()
    quotes_collection = db.quotes
    quotes = quotes_collection.find()
    return render(request, 'quotes/index.html', {'quotes': quotes})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', home, name='home'),
]
