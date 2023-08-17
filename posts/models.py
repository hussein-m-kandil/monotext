from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Post(models.Model):
    text = models.TextField(
        max_length=2048,
        help_text="Type something...",
        validators=[
            MinLengthValidator(2, "Your must type at least 2 characters!"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    text = models.TextField(
        max_length=2048,
        help_text="Comment...",
        validators=[
            MinLengthValidator(2, "Your must type at least 2 characters!"),
        ],
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
