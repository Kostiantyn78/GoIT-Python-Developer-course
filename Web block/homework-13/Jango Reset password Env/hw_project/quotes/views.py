from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import DetailView

from .utils import get_mongodb
from .models import Author

# Create your views here.


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


class AuthorView(DetailView):
    model = Author
    template_name = 'quotes/author.html'
    context_object_name = 'author'
    slug_field = 'fullname'
    slug_url_kwarg = 'author'