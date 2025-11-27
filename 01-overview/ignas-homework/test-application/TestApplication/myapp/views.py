from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
from django.utils import timezone

# LIST all todos
def todo_list(request):
    todos = Todo.objects.all().order_by('resolved', 'due_date')
    return render(request, 'todo_list.html', {'todos': todos})


# CREATE a todo
def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        Todo.objects.create(
            title=title,
            description=description,
            due_date=due_date if due_date else None,
        )
        return redirect('todo_list')

    return render(request, 'todo_form.html')


# EDIT a todo
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)

    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.due_date = request.POST.get('due_date') or None
        todo.save()

        return redirect('todo_list')

    return render(request, 'todo_form.html', {'todo': todo})


# DELETE a todo
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')


# MARK AS RESOLVED
def todo_resolve(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.resolved = True
    todo.save()
    return redirect('todo_list')
