
from .forms import RegisterForm, LoginForm, AuthorForm, QuoteForm
from quotes.utils import get_mongodb
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def add_author_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            db = get_mongodb()
            authors_collection = db.authors
            new_author = {
                'name': form.cleaned_data['name'],
                'bio': form.cleaned_data['bio']
            }
            authors_collection.insert_one(new_author)
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'users/add_author.html', {'form': form})

@login_required
def add_quote_view(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            db = get_mongodb()
            quotes_collection = db.quotes
            new_quote = {
                'author': form.cleaned_data['author'],
                'text': form.cleaned_data['text']
            }
            quotes_collection.insert_one(new_quote)
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'users/add_quote.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')



