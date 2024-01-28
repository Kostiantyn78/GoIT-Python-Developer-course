from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .forms import LoginForm

app_name = "users"

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/',
         LoginView.as_view(template_name='users/login.html', form_class=LoginForm, redirect_authenticated_user=True),
         name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-author', views.add_author, name='add_author'),
    path('add-quote', views.add_quote, name='add_quote'),
]