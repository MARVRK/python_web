from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('add_author/', views.add_author_view, name='add_author'),
    path('add_quote/', views.add_quote_view, name='add_quote'),
]
