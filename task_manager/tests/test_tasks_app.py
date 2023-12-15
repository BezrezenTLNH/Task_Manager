from django.test import TestCase
from task_manager.tasks.models import TaskModel
from task_manager.statuses.models import StatusModel
from task_manager.users.models import Person


class TestTask(TestCase):
    def setUp(self):
        self.user = Person.objects.create(
            first_name="Test",
            last_name="User",
            username="TestUser",
            password="test",
        )
        self.status = StatusModel.objects.create(name="Test Status")
        self.obj = TaskModel.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            author=self.user,
        )

    def test_create_status(self):
        new_obj = TaskModel.objects.create(
            name="Another Test Task",
            description="Another Test Task Description",
            status=self.status,
            author=self.user,
        )

        self.assertEqual(new_obj.name, "Another Test Task")

    def test_read_task(self):
        read_obj = TaskModel.objects.get(id=self.obj.id)

        self.assertEqual(read_obj.name, "Test Task")

    def test_update_task(self):
        self.obj.name = "New Test Task Name"
        self.obj.save()

        updated_obj = TaskModel.objects.get(id=self.obj.id)

        self.assertEqual(updated_obj.name, "New Test Task Name")

    def test_delete_task(self):
        self.obj.delete()

        with self.assertRaises(TaskModel.DoesNotExist):
            TaskModel.objects.get(id=self.obj.id)