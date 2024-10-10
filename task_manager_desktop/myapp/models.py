from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Item(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    time_estimate = models.DurationField(null=True, blank=True)
    history=HistoricalRecords()

    def __str__(self):
        return self.title

class Comment(models.Model):
    task=models.ForeignKey(Item, on_delete=models.CASCADE) #linking comment to a task
    user=models.ForeignKey(User, on_delete=models.CASCADE)#the user who made the comment
    content=models.TextField() #content of the comment
    created_at=models.DateTimeField(auto_now_add=True)#automatic timestamp
    
    def __str__(self):
        return f"comment by {self.user} on {self.task.title}"