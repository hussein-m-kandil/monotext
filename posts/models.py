from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Post(models.Model):
    title = models.CharField(
        default="Untitled Post",
        blank=True,
        max_length=128,
        help_text="Your post's title...",
    )
    text = models.TextField(
        max_length=2048,
        help_text="Your post...",
        validators=[
            MinLengthValidator(2, "Post must have at least 2 characters!"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + '_' + str(self.id)


class Comment(models.Model):
    text = models.TextField(
        max_length=2048,
        help_text="Comment...",
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment on post: {self.post}"
