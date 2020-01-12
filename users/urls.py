from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.register_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('account', views.account_view, name='account')
]
