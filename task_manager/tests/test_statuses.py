from django.contrib.auth.models import User
from django import test
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist

from task_manager.statuses.models import StatusModel


class StatusCodeTestCase(test.TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Jon', password='111')
        self.status = StatusModel.objects.create(name='Status1')

    def test_statuses_url(self):
        self.client._login(self.user)
        response = self.client.get('/statuses/')
        self.assertEqual(response.status_code, 200)

    def test_statuses_url_anonim(self):
        response = self.client.get('/statuses/')
        self.assertRedirects(response, '/login/')

    def test_create_url_anonim(self):
        response = self.client.get('/statuses/create/')
        self.assertRedirects(response, '/login/')

    def test_change_url_anonim(self):
        response = self.client.get(f'/statuses/{self.status.id}/update/')
        self.assertRedirects(response, '/login/')

    def test_delete_url_anonim(self):
        response = self.client.get(f'/statuses/{self.status.id}/delete/')
        self.assertRedirects(response, '/login/')



class StatusesCUDTestCase(test.TestCase):

    def setUp(self):
        self.user = User.objects.create(username='John', password='111')
        self.client._login(self.user)
        self.name_status = {'name': 'Some work'}
        self.upd_name_status = {'name': 'Some upd work'}

    def test_create_status_success(self):
        url = reverse('create_status')
        response = self.client.post(url, self.name_status)
        self.assertRedirects(response, '/statuses/')
        find_status = StatusModel.objects.get(name='Some work')
        self.assertEqual(find_status.name, 'Some work')

    def test_update_status(self):
        status = StatusModel.objects.create(**self.name_status)
        url = reverse('update_status', kwargs={'pk': status.id})
        self.client.post(url, self.upd_name_status)
        update_status = StatusModel.objects.get(id=status.id)
        self.assertEqual(update_status.name, 'Some upd work')

    def test_delete_status_success(self):
        status = StatusModel.objects.create(**self.name_status)
        url = reverse('delete_status', kwargs={'pk': status.id})
        self.client.post(url)

        with self.assertRaises(ObjectDoesNotExist):
            StatusModel.objects.get(id=status.id)
