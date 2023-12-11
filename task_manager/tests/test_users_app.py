from django.contrib.auth.models import User
from django import test
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist


class StatusCodeTestCase(test.TestCase):

    def setUp(self):
        self.logged_user = User.objects.create(username='biba', password='111')
        self.anonim_user = User.objects.create(username='boba', password='222')

    def test_users_url(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_create_url(self):
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, 200)

    def test_change_url_anonim(self):
        response = self.client.get(f'/users/{self.logged_user.id}/update/')
        self.assertRedirects(response, '/login/')

    def test_delete_url_anonim(self):
        response = self.client.get(f'/users/{self.anonim_user.id}/delete/')
        self.assertRedirects(response, '/login/')

class UsersCUDTestCase(test.TestCase):

    def setUp(self):
        self.changeable_user = User.objects.create(
            username='Loki',
            password='111'
        )
        self.data = {
            'valid_user': {
                'username': '@biba1',
                'first_name': 'Alex',
                'last_name': 'Alexeev',
                'password1': '111',
                'password2': '111'
            },
            'updated_valid_user': {
                'username': '/Grishan/',
                'first_mame': 'gRIGORY',
                'last_name': 'Jora',
                'password1': '222',
                'password2': '222',
            },
            'wrong_user_username': {
                'username': '!biba1!',
                'first_name': 'Alex',
                'last_name': 'Alexeev',
                'password1': '111',
                'password2': '111'
            },
            'wrong_user_password': {
                'username': 'JoJora',
                'first_mame': 'Jora',
                'last_name': 'Joestar',
                'password1': '111',
                'password2': '112'
            },
        }

        self.user_data = {
            'first_name': 'JoraJ',
            'last_name': 'Jora',
            'username': 'Jjora',
            'password': '111',
        }

    def test_create_user_success(self):
        url = reverse('create_user')
        user = self.data['valid_user']
        response = self.client.post(url, user)
        self.assertRedirects(response, '/login/')
        find_user = User.objects.get(username='@user')
        self.assertEqual(find_user.username, '@user')

    def test_create_user_false_username(self):
        url = reverse('create_user')
        wrong_user_username = self.data['wrong_user_username']
        self.client.post(url, wrong_user_username)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username='$user')

    def test_create_user_false_password(self):
        url = reverse('create_user')
        wrong_user_password = self.data['wrong_user_password']
        self.client.post(url, wrong_user_password)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username='@user')

    def test_update_user(self):
        user = User.objects.create(**self.user_data)
        self.client._login(user)
        user_pk = user.id
        url = reverse('update_user', kwargs={'pk': user_pk})
        self.client.post(url, self.data['updated_valid_user'])
        update_user = User.objects.get(id=user_pk)
        self.assertEqual(update_user.username, '@master')

    def test_update_user_without_access(self):
        logged_user = User.objects.create(**self.user_data)
        self.client._login(logged_user)
        changeable_user_pk = self.changeable_user.id
        response = self.client.get(f'/users/{changeable_user_pk}/update/')
        self.assertRedirects(response, '/users/')

    def test_delete_user(self):
        user = User.objects.create(**self.user_data)
        self.client._login(user)
        url = reverse('delete_user', kwargs={'pk': user.id})
        self.client.post(url)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=user.id)

    def test_delete_user_without_access(self):
        logged_user = User.objects.create(**self.user_data)
        self.client._login(logged_user)
        deleted_user_pk = self.changeable_user.id
        response = self.client.get(f'/users/{deleted_user_pk}/delete/')
        self.assertRedirects(response, '/users/')
