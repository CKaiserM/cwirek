# Generated by Django 5.1.4 on 2025-02-01 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yard', '0011_alter_commentyard_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='homepage_link',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_bio',
            field=models.CharField(blank=True, max_length=1500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_profile_pic.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='youtube_link',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
