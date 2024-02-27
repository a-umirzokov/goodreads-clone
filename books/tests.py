from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from books.models import Book, BookReview, BookAuthor, Author


class BookListViewTest(TestCase):
    def test_books_list_view(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/list.html')


class BookTests(TestCase):
    def test_book_creation(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.description, 'Test description')
        self.assertEqual(book.isbn, 1000000000000)

    def test_book_list_view(self):
        self.book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/list.html')
        self.assertContains(response, 'Test Book')

    def test_books_list_pagination(self):
        for i in range(10):
            Book.objects.create(
                title=f'Test Book {i}',
                description=f'Test description {i}',
                isbn=1000000000000 + i,
            )
        response = self.client.get('/books/?page=2&page_size=2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/list.html')
        self.assertContains(response, 'Test Book 2')
        self.assertContains(response, 'Test Book 3')
        self.assertNotContains(response, 'Test Book 4')
        self.assertNotContains(response, 'Test Book 1')

    def test_book_detail_view(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        author1 = Author.objects.create(
            first_name='Test',
            last_name='Author',
            email='test@mail.com',
            biography='Test biography'
        )
        author2 = Author.objects.create(
            first_name='Test2',
            last_name='Author2',
            email='test2@mail.com',
            biography='Test2 biography'
        )
        book_author1 = BookAuthor.objects.create(
            book=book,
            author=author1
        )
        book_author2 = BookAuthor.objects.create(
            book=book,
            author=author2
        )
        response = self.client.get(reverse("books:detail", kwargs={'id': book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'Test Author')
        self.assertContains(response, 'Test2 Author2')


class BookReviewTest(TestCase):
    def test_book_review_creation(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        book_review = BookReview.objects.create(
            user=user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        self.assertEqual(book_review.user, user)
        self.assertEqual(book_review.book, book)
        self.assertEqual(book_review.comment, 'Test comment')
        self.assertEqual(book_review.stars_given, 5)

    def test_addreview_view(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        user = CustomUser.objects.create(
            username='akbar',
            first_name='Akbar',
            last_name='Umirzokov',
            email='akbar@mail.com'
        )
        user.set_password('akbar123')
        user.save()
        self.client.login(username='akbar', password='akbar123')

        response = self.client.post(reverse("books:review", kwargs={'id': book.id}), data={
            'stars_given': 5,
            'comment': 'Test comment',
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 5)
        self.assertEqual(book_reviews[0].comment, 'Test comment')
        self.assertEqual(book_reviews[0].user, user)
        self.assertEqual(book_reviews[0].book, book)

    def test_edit_review_view(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        user = CustomUser.objects.create(
            username='akbar',
            first_name='Akbar',
            last_name='Umirzokov',
            email='akbar@gmail.com'
        )
        user.set_password('akbar123')
        user.save()
        book_review = BookReview.objects.create(
            user=user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        self.client.login(username='akbar', password='akbar123')

        edited_comment = 'Edited comment'
        edited_stars = 3
        response = self.client.post(reverse("books:edit_review", kwargs={'book_id': book.id, 'review_id': book_review.id}), data={
            'comment': edited_comment,
            'stars_given': edited_stars
        })
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(book_review.comment, edited_comment)
        self.assertEqual(book_review.stars_given, edited_stars)
        self.assertEqual(book_review.user, user)
        self.assertEqual(book_review.book, book)
        self.assertNotEquals(book_review.comment, 'Test comment')
        self.assertNotEquals(book_review.stars_given, 5)

    def test_delete_review_view(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        user = CustomUser.objects.create(
            username='akbar',
            first_name='Akbar',
            last_name='Umirzokov',
            email='akbar@mail.com'
        )
        user.set_password('akbar123')
        user.save()
        book_review = BookReview.objects.create(
            user=user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        self.client.login(username='akbar', password='akbar123')

        response = self.client.post(reverse("books:delete_review", kwargs={'book_id': book.id, 'review_id': book_review.id}))
        book_reviews = book.bookreview_set.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(book_reviews.count(), 0)
        self.assertNotIn(book_review, book_reviews)
        self.assertNotEqual(book_reviews.count(), 1)
