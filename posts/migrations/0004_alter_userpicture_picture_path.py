# Generated by Django 4.2.4 on 2023-08-25 20:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_userpicture_picture_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpicture',
            name='picture_path',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Something wrong, negative values not allowed!'), django.core.validators.MaxValueValidator(1, 'Something wrong, greater than 1 values not allowed!')]),
        ),
    ]