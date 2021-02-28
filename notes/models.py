from django.db import models

class Note(models.Model):
    num = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(max_length=400, default='')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name