from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from books.models import Book, BookReview, BookAuthor
from books.forms import BookUpdateForm, AddReviewForm


class HomepageView(View):
    def get(self, request):
        reviews = BookReview.objects.all().order_by('-created_at')
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 2)
        p = Paginator(reviews, page_size)
        page_obj = p.get_page(page_number)
        return render(request, 'home.html', {'reviews': reviews, 'page_obj': page_obj})



class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        book_authors = BookAuthor.objects.all()
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(Q(description__icontains=search_query) | Q(title__icontains=search_query))
        print(books)
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 2)
        p = Paginator(books, page_size)
        page_obj = p.get_page(page_number)
        context = {
            'books': page_obj,
            'search_query': search_query,
            'book_authors': book_authors
        }
        return render(request, 'books/list.html', context)



class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = AddReviewForm()
        return render(request, 'books/book_detail.html', {'review_form': review_form, 'book': book})


class BookUpdateView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        form = BookUpdateForm(initial={
            'title': book.title,
            'description': book.description,
            'isbn': book.isbn,
        })
        return render(request, 'books/update.html', {'form': form})

    def post(self, request, id):
        book = Book.objects.get(id=id)
        form = BookUpdateForm(
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            form.save(book)
            messages.success(request, 'Book updated successfully')
            return redirect('books:list')
        else:
            return render(request, 'books/update.html', {'form': form})


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = AddReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save(book, request.user)
            messages.success(request, 'Review added successfully')
            return redirect('books:detail', id=id)
        else:
            return render(request, 'books/book_detail.html', {'review_form': review_form})


class ReviewEditView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = AddReviewForm(initial={
            'comment': review.comment,
            'stars_given': review.stars_given
        })
        context = {
            'form': review_form,
            'book': book,
            'review': review
        }
        return render(request, 'books/review_edit.html', context)

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = AddReviewForm(request.POST)
        if review_form.is_valid():
            review.comment = review_form.cleaned_data['comment']
            review.stars_given = review_form.cleaned_data['stars_given']
            review.save()
            messages.success(request, 'Review updated successfully')
            return redirect('books:detail', id=book_id)
        else:
            return render(request, 'books/review_edit.html', {'form': review_form, 'book': book, 'review': review})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        return render(request, 'books/delete_review.html', {'book': book, 'review': review})

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review.delete()
        messages.success(request, 'Review deleted successfully')
        return redirect('books:detail', id=book_id)
