from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import loader
from django.urls import reverse
from django import forms

from users.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import User


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.clean_email()
            password = form.clean_password2()
            form.save()
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                #messages.add_message(request, messages.SUCCESS, "Vous êtes connecté.")
                return HttpResponseRedirect(reverse('home'))

        #else:
            #messages.add_message(request, messages.ERROR, "Cet email est déjà utilisé. Veuillez recommencer.")
            #if form.clean_password2() == forms.ValidationError:
                #messages.add_message(request, messages.ERROR, "Les mots de passe ne correspondent pas. Veuillez recommencer.")
            #else:
                #messages.add_message(request, messages.ERROR, "Cet email est déjà utilisé. Veuillez recommencer.")

    else:
        form = RegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #messages.add_message(request, messages.SUCCESS, "Vous êtes connecté.")
                else:
                    messages.add_message(request, messages.ERROR, "Compte désactivé.")
            else:
                messages.add_message(
                    request, messages.ERROR, "L'email et/ou le mot de passe sont invalides. Veuillez saisir à nouveau vos identifiants ou créer un compte.")
                return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def account_view(request):
    template = loader.get_template('users/account.html')
    return HttpResponse(template.render(request=request))

