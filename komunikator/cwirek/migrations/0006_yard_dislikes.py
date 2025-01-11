# Generated by Django 5.1.4 on 2025-01-11 21:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cwirek', '0005_yard_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='yard',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='yard_dislike', to=settings.AUTH_USER_MODEL),
        ),
    ]
