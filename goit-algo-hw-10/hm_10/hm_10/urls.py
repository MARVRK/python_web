from django.contrib import admin
from django.urls import path, include
from quotes.utils import get_mongodb
from django.shortcuts import render

def home(request):
    db = get_mongodb()
    quotes_collection = db.quotes
    quotes = list(quotes_collection.find())
    return render(request, 'quotes/index.html', {'quotes': quotes})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', home, name='home'),
]
