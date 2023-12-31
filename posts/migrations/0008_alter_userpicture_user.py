# Generated by Django 4.2.4 on 2023-08-27 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0007_alter_userpicture_picture_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpicture',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_picture', to=settings.AUTH_USER_MODEL),
        ),
    ]
