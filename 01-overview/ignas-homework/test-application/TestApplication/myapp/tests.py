from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TodoTests(TestCase):

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_list.html')

    def test_create_todo(self):
        response = self.client.post(reverse('todo_create'), {
            'title': 'Test task',
            'description': 'Testing create',
            'due_date': '2025-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)

    def test_edit_todo(self):
        todo = Todo.objects.create(title="Old title")
        response = self.client.post(reverse('todo_edit', args=[todo.id]), {
            'title': 'Updated title',
            'description': '',
            'due_date': ''
        })
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated title')

    def test_delete_todo(self):
        todo = Todo.objects.create(title="Delete me")
        response = self.client.get(reverse('todo_delete', args=[todo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_resolve_todo(self):
        todo = Todo.objects.create(title="Resolve me")
        response = self.client.get(reverse('todo_resolve', args=[todo.id]))
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertTrue(todo.resolved)

    def test_str_representation(self):
        todo = Todo.objects.create(title="My title")
        self.assertEqual(str(todo), "My title")
