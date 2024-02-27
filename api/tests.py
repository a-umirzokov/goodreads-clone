from django.urls import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
    def test_get_book_review(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        book_review = BookReview.objects.create(
            user=self.user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        response = self.client.get(reverse("api:review-detail", kwargs={'id': book_review.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['comment'], 'Test comment')
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['book']['title'], 'Test Book')
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_get_book_reviews(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )
        self.client.login(username='testuser2', password='testpassword2')
        book_review = BookReview.objects.create(
            user=self.user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        book_review2 = BookReview.objects.create(
            user=user2,
            book=book,
            comment='Test comment2',
            stars_given=3
        )
        response = self.client.get(reverse("api:review-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(response.data['results'][0]['comment'], 'Test comment2')
        self.assertEqual(response.data['results'][0]['stars_given'], 3)
        self.assertEqual(response.data['results'][0]['book']['title'], 'Test Book')
        self.assertEqual(response.data['results'][0]['user']['username'], 'testuser2')
        self.assertEqual(response.data['results'][1]['stars_given'], 5)
        self.assertEqual(response.data['results'][1]['book']['title'], 'Test Book')
        self.assertEqual(response.data['results'][1]['user']['username'], 'testuser')
        self.assertEqual(response.data['results'][1]['comment'], 'Test comment')

    def test_post_review(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=1000000000000,
        )
        response = self.client.post(reverse("api:review-list"), data={
            'user_id': self.user.id,
            'book_id': book.id,
            'comment': 'Test comment',
            'stars_given': 5
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['comment'], 'Test comment')
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['book']['title'], 'Test Book')
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_put_review(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=10099,
        )
        book_review = BookReview.objects.create(
            user=self.user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        response = self.client.put(reverse("api:review-detail", kwargs={'id': book_review.id}), data={
            'user_id': self.user.id,
            'book_id': book.id,
            'comment': 'Test comment2',
            'stars_given': 3
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['comment'], 'Test comment2')
        self.assertEqual(response.data['stars_given'], 3)
        self.assertEqual(response.data['book']['title'], 'Test Book')
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_patch_review(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=10099,
        )
        book_review = BookReview.objects.create(
            user=self.user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        response = self.client.patch(reverse("api:review-detail", kwargs={'id': book_review.id}), data={
            'comment': 'Test comment2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['comment'], 'Test comment2')
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['book']['title'], 'Test Book')
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_delete_review(self):
        book = Book.objects.create(
            title='Test Book',
            description='Test description',
            isbn=10099,
        )
        book_review = BookReview.objects.create(
            user=self.user,
            book=book,
            comment='Test comment',
            stars_given=5
        )
        response = self.client.delete(reverse("api:review-detail", kwargs={'id': book_review.id}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BookReview.objects.count(), 0)
