from django.db import models

# Create your models here.

class Room(models.Model):
    # hosts
    # topic
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # participants
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name