# Generated by Django 4.2.4 on 2023-08-25 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_userpicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpicture',
            name='picture_path',
            field=models.CharField(max_length=512),
        ),
    ]
