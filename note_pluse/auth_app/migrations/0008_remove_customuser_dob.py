# Generated by Django 5.0.2 on 2024-02-20 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0007_alter_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='dob',
        ),
    ]
