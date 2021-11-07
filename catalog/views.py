from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
from .models import Book, Author, BookInstance, Genre

@login_required()
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


# class BookListView(generic.ListView):
#     model = Book
#     context_object_name = 'book_list'   # your own name for the list as a template variable
#     queryset = Book.objects.all() # Get 5 books containing the title war
#     template_name = 'book_list.html'

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 2



    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 2



    def get_queryset(self):
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
