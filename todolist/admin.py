from django.contrib import admin

# Register your models here.
from todolist.models import TodoList

admin.site.register(TodoList)
