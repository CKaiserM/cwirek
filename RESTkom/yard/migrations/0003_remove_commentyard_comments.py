# Generated by Django 5.1.4 on 2025-01-26 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yard', '0002_commentyard_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentyard',
            name='comments',
        ),
    ]
