from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TodoList(models.Model):
    title = models.CharField(max_length=250)  # a varchar
    content = models.TextField(blank=True)  # a text field
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # a date
    completed = models.NullBooleanField(null=True, blank=True, default=False)
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))  # a date
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]  # ordering by the created field

    def __str__(self):
        return self.title  # name to be shown when called
