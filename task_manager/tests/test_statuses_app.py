from django.test import TestCase
from task_manager.statuses.models import StatusModel


class TestLabel(TestCase):
    def setUp(self):
        self.obj = StatusModel.objects.create(name="Test Status")

    def test_create_status(self):
        new_obj = StatusModel.objects.create(name="Another Test Status")

        self.assertEqual(new_obj.name, "Another Test Status")

    def test_read_status(self):
        read_obj = StatusModel.objects.get(id=self.obj.id)

        self.assertEqual(read_obj.name, "Test Status")

    def test_update_status(self):
        self.obj.name = "New Test Status Name"
        self.obj.save()

        updated_obj = StatusModel.objects.get(id=self.obj.id)

        self.assertEqual(updated_obj.name, "New Test Status Name")

    def test_delete_status(self):
        self.obj.delete()

        with self.assertRaises(StatusModelDoesNotExist):
            StatusModel.objects.get(id=self.obj.id)