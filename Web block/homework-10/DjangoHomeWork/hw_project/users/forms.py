from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, CharField, TextInput, EmailInput, EmailField, PasswordInput, Textarea,\
    ModelChoiceField, Select
from .models import Author, Quote


class RegisterForm(UserCreationForm):
    username = CharField(max_length=16, min_length=3, required=True, widget=TextInput(attrs={"class": "form-control"}))
    email = EmailField(max_length=25, required=True, widget=EmailInput(attrs={"class": "form-control"}))
    password1 = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))
    password2 = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = CharField(max_length=16, min_length=3, required=True, widget=TextInput(attrs={"class": "form-control"}))
    password = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'password')


class AddAuthorForm(ModelForm):
    fullname = CharField(max_length=50, min_length=2, required=True, widget=TextInput(attrs={"class": "form-control","id": "exampleInputEmail1"}))
    born_date = CharField(max_length=50, min_length=2, required=True, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))
    born_location = CharField(max_length=150, min_length=2, required=True, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))
    description = CharField(widget=Textarea)

    class Meta:
        model = Author
        fields = ('fullname', 'born_date', 'born_location', 'description')


class AddQuoteForm(ModelForm):
    quote = CharField(widget=Textarea)
    author = ModelChoiceField(Author.objects.all(), widget=Select(attrs={"class": "form-select"}))

    class Meta:
        model = Quote
        fields = ('quote', 'author')

