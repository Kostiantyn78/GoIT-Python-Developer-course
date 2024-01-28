from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import logout
from django.contrib import messages

from .forms import RegisterForm, AddAuthorForm, AddQuoteForm
from .models import Author, Quote


# Create your views here.


class RegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:root")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Congratulations {username}. Your account has been successfully created.")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have logged out of your account')
    return redirect('/page/1')


@login_required
def add_author(request):
    form = AddAuthorForm(instance=Author())
    if request.method == 'POST':
        form = AddAuthorForm(request.POST, instance=Author())
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
            return redirect(to='/page/1')
    return render(request, 'users/add_author.html', context={"form": form})


@login_required
def add_quote(request):
    form = AddQuoteForm(instance=Quote())
    if request.method == 'POST':
        form = AddQuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            return redirect(to='/page/1')
    return render(request, 'users/add_quote.html', context={"form": form})