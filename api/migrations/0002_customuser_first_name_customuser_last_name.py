# Generated by Django 5.0.6 on 2024-10-17 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.TextField(default=''),
        ),
    ]
