# Generated by Django 5.1.4 on 2025-01-10 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cwirek', '0003_yard'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
