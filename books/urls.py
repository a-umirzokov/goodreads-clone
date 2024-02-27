from django.conf.urls.static import static
from django.urls import path
from books import views as v
from goodreads import settings

app_name = 'books'
urlpatterns = [
    path('', v.HomepageView.as_view(), name='home'),
    path('books/', v.BookListView.as_view(), name='list'),
    path('books/<int:id>', v.BookDetailView.as_view(), name='detail'),
    path('books/<int:id>/review', v.AddReviewView.as_view(), name='review'),
    path('books/<int:id>/update', v.BookUpdateView.as_view(), name='update'),
    path('books/<int:book_id>/review/<int:review_id>/edit', v.ReviewEditView.as_view(), name='edit_review'),
    path('books/<int:book_id>/review/<int:review_id>/delete', v.DeleteReviewView.as_view(), name='delete_review'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
