from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import loader
from django.urls import reverse

from users.forms import RegistrationForm, LoginForm, DivErrorList
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            email = form.clean_email()
            password = form.clean_password2()
            form.save()
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Votre compte a été créé', extra_tags='toaster')
                return HttpResponseRedirect(reverse('home'))

    else:
        form = RegistrationForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Vous êtes connecté', extra_tags='toaster')
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.add_message(request, messages.ERROR, "Compte désactivé.")
                    return HttpResponseRedirect(reverse('login'))

        messages.add_message(
            request, messages.ERROR, "L'email et/ou le mot de passe sont invalides. Veuillez saisir à nouveau vos identifiants ou créer un compte.")
        messages.error(request, 'Erreur de saisie', extra_tags='toaster')
        return HttpResponseRedirect(reverse('login'))

    else:
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté', extra_tags='toaster')
    return HttpResponseRedirect(reverse('home'))


def account_view(request):
    template = loader.get_template('users/account.html')
    return HttpResponse(template.render(request=request))

