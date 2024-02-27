from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTest(TestCase):
    def test_user_account_is_created(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

        self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'ut@mail.com',
                'password': 'testpassword',
            }
        )

        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'ut@mail.com')
        self.assertNotEquals(user.password, 'testpassword')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.groups.count(), 0)
        self.assertEqual(user.user_permissions.count(), 0)

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'tu@mail.uz',
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'tu@mailuz',
                'password': 'testpassword',
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        CustomUser.objects.create_user(
            username='testuser',
            first_name='Test',
            password='testpassword',
        )

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'testuser',
                'first_name': 'Test',
                'password': 'testpassword',
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTest(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create_user(
            username='testuser',
            first_name='Test',
        )
        self.db_user.set_password('testpassword')
        self.db_user.save()

    def test_successful_login(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                'username': 'testuser',
                'password': 'testpassword',
            }
        )
        self.assertRedirects(response, reverse('books:home'))
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wronguser',
                'password': 'testpassword',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'testuser',
                'password': 'wrongpassword',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('books:home'))
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 302)


class ProfileTest(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='tu@mail.uz'
        )
        self.db_user.set_password('testpassword')
        self.db_user.save()

    def test_user_profile_redirect(self):
        response = self.client.get(reverse('users:profile'))
        self.assertRedirects(response, reverse('users:login')+f'?next={reverse("users:profile")}')
        self.assertEqual(response.status_code, 302)

    def test_user_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:profile'))
        user = response.context['user']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_user_update(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:update'))
        user = response.context['user']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

        self.client.post(
            reverse('users:update'),
            data={
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'tu@gmail.com',
            }
        )
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.email, 'tu@gmail.com')
