from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # If the user is deleted, delete their posts
        related_name='blog_posts'  # Allows reverse access to posts from user
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) # Automatically set when the object is created
    updated = models.DateTimeField(auto_now=True) # Automatically set when the object is updated
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Custom manager for published posts
    class Meta:
        ordering = ('-publish',)  # Order by publish date, newest first
        indexes =[
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
    