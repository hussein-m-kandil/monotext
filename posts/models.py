from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Post(models.Model):
    title = models.CharField(
        default="Untitled Post",
        max_length=128,
        help_text="Your post's title...",
        validators=[
            MinLengthValidator(1, "Your must type at least 2 characters!"),
        ],
    )
    text = models.TextField(
        max_length=2048,
        help_text="Your post...",
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
            MinLengthValidator(1, "Your must type at least 2 characters!"),
        ],
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
