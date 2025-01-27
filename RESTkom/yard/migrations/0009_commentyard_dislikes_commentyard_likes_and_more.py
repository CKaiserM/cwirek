# Generated by Django 5.1.4 on 2025-01-27 23:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yard', '0008_alter_commentyard_yard'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commentyard',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='comment_dislike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentyard',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='replytoyardcomment',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='reply_dislike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='replytoyardcomment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='reply_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
