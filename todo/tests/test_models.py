from todo.models import Todo
from utils.setup_test import TestSetup


class TestModel(TestSetup):

    def test_should_create_todo_with_user(self):
        user = self.create_test_user()
        todo = Todo.objects.create(title="title", description="description", owner=user)
        todo.save()

        self.assertEqual(str(todo), "title")