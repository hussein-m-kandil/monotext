# Generated by Django 4.2.4 on 2023-08-19 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_comment_text_alter_post_text_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, default='Untitled Post', help_text="Your post's title...", max_length=128, validators=[django.core.validators.MinLengthValidator(1, 'Title must have at least 1 characters!')]),
        ),
    ]