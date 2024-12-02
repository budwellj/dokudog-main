from django.db import models

# Create your models here.

class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Work(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    difficulty = models.IntegerField()
    themes = models.ManyToManyField(Theme, related_name="works")
    # Additional fields as needed

    def __str__(self):
        return self.title

