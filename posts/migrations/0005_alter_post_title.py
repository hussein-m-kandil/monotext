# Generated by Django 4.2.4 on 2023-08-19 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, default='Untitled Post', help_text="Your post's title...", max_length=128),
        ),
    ]
