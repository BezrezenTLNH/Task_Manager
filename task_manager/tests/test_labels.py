from django.test import TestCase
from django import test
from task_manager.labels.models import LabelModel


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TestLabel(TestCase):
    def setUp(self):
        self.obj = LabelModel.objects.create(name="Test Label")

    def test_create_label(self):
        new_obj = LabelModel.objects.create(name="Second Test Label")

        self.assertEqual(new_obj.name, "Second Test Label")

    def test_read_label(self):
        read_obj = LabelModel.objects.get(id=self.obj.id)

        self.assertEqual(read_obj.name, "Test Label")

    def test_update_label(self):
        self.obj.name = "New Test Label Name"
        self.obj.save()

        updated_obj = LabelModel.objects.get(id=self.obj.id)

        self.assertEqual(updated_obj.name, "New Test Label Name")

    def test_delete_label(self):
        self.obj.delete()

        with self.assertRaises(LabelModel.DoesNotExist):
            LabelModel.objects.get(id=self.obj.id)
